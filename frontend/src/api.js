import axios from 'axios';

const API_BASE_URL = '/api/v1'; // Adjust to match your backend's URL and port

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Ensures cookies (session) are sent with requests
});

// Helper function to handle errors
const handleError = (error) => {
  if (error.response) {
    console.error('API Error:', error.response.data);
    throw new Error(error.response.data.detail || 'An error occurred');
  } else {
    console.error('Network Error:', error.message);
    throw new Error('Network error occurred. Please try again.');
  }
};

// API Functions
export const login = async () => {
  try {
    const { data } = await apiClient.get('/login');
    return data.auth_url; // Redirect the user to this URL for authentication
  } catch (error) {
    handleError(error);
  }
};

export const logout = async () => {
  try {
    await apiClient.get('/logout');
    return { message: 'Successfully logged out' };
  } catch (error) {
    handleError(error);
  }
};

export const getProfile = async () => {
  try {
    const { data } = await apiClient.get('/profile');
    return data; // { name, email, picture }
  } catch (error) {
    handleError(error);
  }
};

export const chat = async (messages) => {
  try {
    const { data } = await apiClient.post('/chat', { messages });
    return data; // { reply, videos }
  } catch (error) {
    handleError(error);
  }
};

export const addToLibrary = async (ytLink) => {
  try {
    const { data } = await apiClient.post('/library', { yt_link: ytLink });
    return data; // { message, video }
  } catch (error) {
    handleError(error);
  }
};

export const getLibrary = async () => {
  try {
    const { data } = await apiClient.get('/library');
    return data.videos; // Array of videos
  } catch (error) {
    handleError(error);
  }
};

export const watch = async (ytLink) => {
  try {
    const { data } = await apiClient.get('/watch', { params: { yt_link: ytLink } });
    return data; // { outline, quiz }
  } catch (error) {
    handleError(error);
  }
};
