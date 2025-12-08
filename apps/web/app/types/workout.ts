export interface Exercise {
  name: string;
  sets: number;
  reps: string;
  rest: string;
}

export interface WorkoutDay {
  day: number;
  focus: string;
  duration_minutes: number;
  equipment: string[];
  warmup: string;
  exercises: Exercise[];
  cooldown: string;
  estimated_calories: number;
}

export interface WorkoutProgram {
  program: WorkoutDay[];
}