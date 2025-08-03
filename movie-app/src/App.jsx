"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Star } from "lucide-react"

export default function MovieRecommender() {
  const [input, setInput] = useState("")
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(false)

  const fetchRecommendations = async () => {
    if (!input.trim()) return
    setLoading(true)

    try {
      // Send movie title to Flask backend
      const res = await fetch("https://movie-recommender-bit5.onrender.com/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ movie: input }),
      })

      const result = await res.json();
const recommendedTitles = result.recommendations;
console.log("Received titles:", recommendedTitles);



      // Fetch OMDb details for each recommended title
      const omdbPromises = recommendedTitles.map(async (title) => {
        const omdbRes = await fetch(
          `https://www.omdbapi.com/?t=${encodeURIComponent(title)}&apikey=2cb5fade`
        )
        return await omdbRes.json()
      })

      const detailedMovies = await Promise.all(omdbPromises)
      setMovies(detailedMovies)
    } catch (err) {
      console.error("Error fetching recommendations:", err)
      alert("Something went wrong while fetching recommendations.")
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-gray-100 p-4 sm:p-8 text-center flex flex-col items-center">
      <h1 className="text-4xl font-extrabold text-white mb-8 tracking-tight">🎬 Movie Recommender</h1>

      <div className="flex flex-col sm:flex-row justify-center gap-3 mb-10 w-full max-w-md">
        <Input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter a movie title"
          className="flex-grow px-4 py-2 border border-zinc-700 bg-zinc-800 text-gray-100 placeholder-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 shadow-sm"
        />
        <Button
          onClick={fetchRecommendations}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-zinc-950 transition-all duration-200 shadow-md"
          disabled={loading}
        >
          {loading ? "Loading..." : "Recommend"}
        </Button>
      </div>

      {loading && <p className="text-lg text-gray-400 mb-6">Fetching recommendations...</p>}

      <div className="grid grid-cols-1 gap-6 w-full max-w-4xl mx-auto">
        {movies.map((movie, i) => (
          <Card
            key={i}
            className="bg-zinc-900 rounded-2xl shadow-lg overflow-hidden flex flex-col md:flex-row border border-zinc-800"
          >
            <div className="flex-shrink-0 w-full md:w-64 h-48 md:h-auto">
              <img
                src={movie.Poster !== "N/A" ? movie.Poster : "/placeholder.svg"}
                alt={movie.Title}
                className="w-full h-full object-cover rounded-t-2xl md:rounded-l-2xl md:rounded-tr-none"
              />
            </div>
            <div className="flex flex-col p-4 flex-grow">
              <CardHeader className="pb-2 px-0 pt-0">
                <CardTitle className="text-xl font-semibold text-white line-clamp-1">{movie.Title}</CardTitle>
                <CardDescription className="text-sm text-gray-400 flex items-center gap-1">
                  {movie.Genre} • <Star className="size-4 text-yellow-500 fill-yellow-500" />{" "}
                  {movie.imdbRating} • {movie.Year}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-grow px-0 pb-0">
                <p className="text-sm text-gray-300 line-clamp-3">{movie.Plot}</p>
              </CardContent>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
