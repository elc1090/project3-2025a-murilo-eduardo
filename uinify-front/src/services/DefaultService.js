import axiosService from "src/services/interceptors/AxiosService";

export const getUsers = (id) => axiosService.get(`/users`);

export const getUserById = (id) => axiosService.get(`/users/${id}`);

export const getUserComponents = (id) =>
  axiosService.get(`/user/${id}/components`);

export const getComponents = () => axiosService.get(`/components`);

export const getComponentById = (id) => axiosService.get(`/component/${id}`);

export const saveComponent = (payload) =>
  axiosService.post(`/component`, payload);

export const updateComponent = (id, payload) =>
  axiosService.put(`/component/${id}`, payload);

export const deleteComponent = (id) => axiosService.delete(`/component/${id}`);

export const login = (payload) => axiosService.post("/login", payload);
