import { WorkoutDay } from "@/app/types/workout";

const equipmentIcons: Record<string, string> = {
  barbell: "🏋️",
  dumbbell: "💪",
  dumbbells: "💪",
  bench: "🪑",
  "pull-up bar": "🔩",
  pullup_bar: "🔩",
  mat: "🧘",
  yoga_mat: "🧘",
  none: "👐",
  bodyweight: "🤸",
  kettlebell: "🔔",
  resistance_bands: "🎗️",
  treadmill: "🏃",
  bike: "🚴",
  cable_machine: "⚙️",
};

function getEquipmentIcon(equipment: string): string {
  const key = equipment.toLowerCase().replace(/\s+/g, "_");
  return equipmentIcons[key] || "🏋️";
}

export default function WorkoutCard({ workout }: { workout: WorkoutDay }) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
      {/* Header */}
      <div className="bg-linear-to-r from-blue-600 to-blue-700 p-4 text-white">
        <h3 className="text-xl font-bold">Day {workout.day}</h3>
        <p className="text-blue-100">{workout.focus}</p>
      </div>

      {/* Meta info */}
      <div className="p-4 border-b flex justify-between text-sm text-gray-600">
        <span>⏱️ {workout.duration_minutes} min</span>
        <span>🔥 {workout.estimated_calories} kcal</span>
      </div>

      {/* Equipment */}
      <div className="px-4 py-2 bg-gray-50 flex gap-2 flex-wrap">
        {workout.equipment.map((eq, i) => (
          <span
            key={i}
            className="px-2 py-1 bg-white rounded text-sm shadow-sm"
          >
            {getEquipmentIcon(eq)} {eq}
          </span>
        ))}
      </div>

      {/* Warmup */}
      <div className="px-4 py-2 text-sm border-b">
        <span className="font-medium text-orange-600">🔥 Warmup: </span>
        {workout.warmup}
      </div>

      {/* Exercises */}
      <div className="p-4">
        <h4 className="font-semibold mb-3">Exercises</h4>
        <div className="space-y-2">
          {workout.exercises.map((ex, i) => (
            <div
              key={i}
              className="flex justify-between items-center text-sm p-2 bg-gray-50 rounded"
            >
              <span className="font-medium">{ex.name}</span>
              <span className="text-gray-600 text-xs">
                {ex.sets} × {ex.reps} | Rest: {ex.rest}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Cooldown */}
      <div className="px-4 py-3 text-sm border-t bg-blue-50">
        <span className="font-medium text-blue-600">❄️ Cooldown: </span>
        {workout.cooldown}
      </div>
    </div>
  );
}