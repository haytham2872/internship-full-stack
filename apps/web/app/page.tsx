import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-linear-to-br from-blue-600 to-blue-800 flex items-center justify-center">
      <div className="text-center text-white px-4">
        <h1 className="text-5xl font-bold mb-4">🏋️ Workout Generator</h1>
        <p className="text-xl text-blue-100 mb-8 max-w-md mx-auto">
          Generate personalized workout programs powered by AI. Just describe
          your goals and let us create the perfect plan for you.
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
          >
            Login
          </Link>
          <Link
            href="/signup"
            className="px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-400 transition-colors border border-blue-400"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
}