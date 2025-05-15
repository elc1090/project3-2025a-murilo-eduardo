import axios from "axios";
import { Environment } from "src/environment/environment";

const axiosService = axios.create({
  baseURL: Environment.baseUrl,
  headers: {
    "Content-Type": "application/json",
    Authorization: `Token ${Environment.token}`,
  },
});

export default axiosService;
