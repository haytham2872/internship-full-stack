"use client";

import { useState } from "react";
import { useAuth } from "@/app/context/AuthContext";
import ProtectedRoute from "@/app/components/ProtectedRoute";
import WorkoutCard from "@/app/components/WorkoutCard";
import { WorkoutProgram } from "@/app/types/workout";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function GeneratePage() {
  const { token, user, logout } = useAuth();
  const [input, setInput] = useState("");
  const [program, setProgram] = useState<WorkoutProgram | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateProgram = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${API_URL}/api/ai/program`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text: input }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to generate program");
      }

      const data = await res.json();
      setProgram(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  const downloadJSON = () => {
    if (!program) return;
    const blob = new Blob([JSON.stringify(program, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "workout-program.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <Link href="/dashboard" className="text-xl font-bold text-gray-800">
              ← Back to Dashboard
            </Link>
            <div className="flex items-center gap-4">
              <span className="text-gray-600">{user?.email}</span>
              <button
                onClick={logout}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold mb-8">Generate Workout Program</h1>

          {/* Input Section */}
          <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe your workout goals
            </label>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Example: I want to lose weight, 4 sessions/week, 45 min each, no dumbbells, intermediate level. Focus on cardio and core strength."
              className="w-full h-32 p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <div className="flex flex-wrap gap-4 mt-4">
              <button
                onClick={generateProgram}
                disabled={loading || !input.trim()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <span className="animate-spin">⏳</span> Generating...
                  </span>
                ) : (
                  "🚀 Generate"
                )}
              </button>

              {program && (
                <>
                  <button
                    onClick={generateProgram}
                    disabled={loading}
                    className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 transition-colors"
                  >
                    🔄 Re-generate
                  </button>
                  <button
                    onClick={downloadJSON}
                    className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    📥 Download JSON
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Error display */}
          {error && (
            <div className="mb-8 p-4 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {/* Program Grid */}
          {program && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {program.program
                .sort((a, b) => a.day - b.day)
                .map((day) => (
                  <WorkoutCard key={day.day} workout={day} />
                ))}
            </div>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}