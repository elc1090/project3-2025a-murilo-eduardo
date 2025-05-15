import { defineStore } from "pinia";

const defaultData = [];

export const getExerciseStorage = () => {
  const string = localStorage.getItem("exercise-storage");

  if (!string) {
    return defaultData;
  }

  try {
    return JSON.parse(string);
  } catch (error) {
    console.error("Erro ao parsear exercise-storage do localStorage:", error);
    return defaultData;
  }
};

export const useExerciseStorage = defineStore("exercise-storage", {
  state: () => ({ data: getExerciseStorage() }),
  actions: {
    save(data) {
      this.data = data;
      localStorage.setItem("exercise-storage", JSON.stringify(this.data));
    },
    remove() {
      this.data = defaultData;
      localStorage.removeItem("exercise-storage");
    },
  },
});
