import { defineStore } from "pinia";

const defaultData = {
  user: null,
};

export const getAuthStorage = () => {
  const authString = localStorage.getItem("UInify-auth");

  if (!authString) {
    return defaultData;
  }

  try {
    return JSON.parse(authString);
  } catch (error) {
    console.error("Erro ao parsear UInify-auth do localStorage:", error);
    return defaultData;
  }
};

export const useAuthStore = defineStore("UInify-auth", {
  state: () => ({ authData: getAuthStorage() }),
  getters: {
    storeAuthDataGetter(state) {
      return state.authData;
    },
  },
  actions: {
    storageAuthSave(auth) {
      this.authData = auth;
      localStorage.setItem("UInify-auth", JSON.stringify(this.authData));
    },
    storageAuthRemove() {
      this.authData = defaultData;
      localStorage.removeItem("UInify-auth");
    },
  },
});
