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
    const authUrl = data.auth_url;
    window.location.href = authUrl;
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
    return { response: data, err: null };
  } catch (error) {
    handleError(error);
  }
};

export const recommendVideos = async (messages) => {
  try {
    return {
  "reply": {
    "role": "assistant",
    "content": "Given your decade of experience in software engineering, including system programming and web development,  the beginner-level Rust tutorials are likely unnecessary.  Jumping straight into the \"Learn Rust Programming - Complete Course\" is a viable option.  Its comprehensive nature will cover the fundamentals efficiently, leveraging your existing programming knowledge.\n\nThe course covers a wide range of topics including ownership, borrowing, and advanced concepts like lifetimes and iterators.  These are areas where your prior experience might not fully translate, and the video's structured approach will be beneficial.\n\nThe \"Rust Project Tutorial – Authentication Server Using Warp + JWT\" is best left for after you've solidified your understanding from the complete course.  While you could potentially attempt it now, the learning curve could be steeper than expected, potentially leading to frustration.  Completing the \"Learn Rust Programming - Complete Course\" first ensures you possess the necessary foundational skills for this project.\n\nThe \"System Design Concepts Course and Interview Prep\" is entirely separate.  It focuses on system architecture, not Rust itself.  While relevant to your broader career goals, it shouldn't be prioritized before gaining fluency in Rust's core features. You can consider this course once you feel confident working with Rust on smaller to medium sized projects.\n\n**Recommendation:** Begin with \"Learn Rust Programming - Complete Course\".  Use it as a deep dive to master Rust's unique features.  Once finished,  move onto the authentication server project. The system design course can be pursued concurrently or later, depending on your career priorities.\n"
  },
  "videos": [
    {
      "video_id": "BpPEoZW5IiY",
      "url": "https://www.youtube.com/watch?v=BpPEoZW5IiY",
      "description": "In this comprehensive Rust course for beginners, you will learn about the core concepts of the language and underlying mechanisms in theory.\n\n✏️ Course developed by @zubiarfan \n\n🔗 Rust by Practice: https://practice.rs/\n🔗 Code: https://github.com/3rfaan/courses/tree/main/Rust/rust-by-practice/src\n\n⭐️ Contents ⭐️\n00:00:00 Introduction & Learning Resources\n00:06:19 Variables\n00:27:07 Numbers & Binary System\n01:09:51 Chars, Bools & Unit Types\n01:17:55 Statements & Expressions\n01:24:50 Functions\n01:32:53 Ownership\n02:24:06 Borrowing\n02:47:45 String vs. &str\n03:17:59 Slices\n03:31:35 Tuples\n03:40:04 Structs\n04:02:52 Enums\n04:13:46 The \"Option\" Enum\n04:21:32 Flow Control\n04:44:43 Pattern Match\n05:16:42 Methods & Associated Functions\n05:31:50 Generics\n06:06:32 Traits\n06:47:15 Trait Objects\n07:09:51 Associated Types\n07:39:31 String\n07:59:52 Vectors\n08:29:00 HashMaps\n08:52:45 Type Coercion\n09:04:54 From & Into\n09:36:03 panic!\n09:44:56 Result\n10:28:23 Cargo, Crates & Modules\n11:08:28 Debug & Display\n11:30:13 Lifetimes\n12:14:46 Lifetime Elision\n12:38:53 Closures\n13:30:08 Iterators\n\nCorrection:\n12:53:20 Because of the `move` keyword the closure actually takes ownership of the `movable` variable, not an immutable reference. The reason we can call the closure twice is because the `movable` variable INSIDE the closure is the owner of the data. Meaning we can call the closure any number of times.\n\n🎉 Thanks to our Champion and Sponsor supporters:\n👾 davthecoder\n👾 jedi-or-sith\n👾 南宮千影\n👾 Agustín Kussrow\n👾 Nattira Maneerat\n👾 Heather Wcislo\n👾 Serhiy Kalinets\n👾 Justin Hual\n👾 Otis Morgan\n\n--\n\nLearn to code for free and get a developer job: https://www.freecodecamp.org\n\nRead hundreds of articles on programming: https://freecodecamp.org/news",
      "title": "Learn Rust Programming - Complete Course 🦀",
      "thumbnail_url": "https://i.ytimg.com/vi/BpPEoZW5IiY/hqdefault.jpg",
      "outline": null
    },
    {
      "video_id": "6oMoHZZeyb0",
      "url": "https://www.youtube.com/watch?v=6oMoHZZeyb0",
      "description": "In this course, you will learn how to use Rust to create an authentication server. The course provides a comprehensive guide on user data management, structure, and token-based authentication. Special attention is given to error handling, JWT issues, and practical solutions for common challenges. Concluding with a hands-on demo, viewers will gain a thorough understanding of token creation and user management in modern applications\n\n✏️ Course created by @AkhilSharmaTech \n\n0:00:00 Introduction and setup\n0:06:42 Admin and user authentication\n0:15:53 User data handling and roles\n0:28:54 Introduction to user structures and attributes\n0:45:41 Token management and claims analysis\n1:01:48 Deep dive into roles and tokens\n1:05:03 Error handling and permissions\n1:14:58 Advanced error insights and JWT issues\n1:29:19 Code analysis and issue resolution\n1:31:24 Final touches and RS file exploration\n1:34:50 Demo review and token creation\n\n\n🎉 Thanks to our Champion and Sponsor supporters:\n👾 davthecoder\n👾 jedi-or-sith\n👾 南宮千影\n👾 Agustín Kussrow\n👾 Nattira Maneerat\n👾 Heather Wcislo\n👾 Serhiy Kalinets\n👾 Justin Hual\n👾 Otis Morgan \n👾 Oscar Rahnama\n\n--\n\nLearn to code for free and get a developer job: https://www.freecodecamp.org\n\nRead hundreds of articles on programming: https://freecodecamp.org/news",
      "title": "Rust Project Tutorial – Authentication Server Using Warp + JWT",
      "thumbnail_url": "https://i.ytimg.com/vi/6oMoHZZeyb0/hqdefault.jpg",
      "outline": null
    },
    {
      "video_id": "F2FmTdLtb_4",
      "url": "https://www.youtube.com/watch?v=F2FmTdLtb_4",
      "description": "This complete system design tutorial covers scalability, reliability, data handling, and high-level architecture with clear explanations, real-world examples, and practical strategies. You will learn the core concepts you need to know for a system designs interview.\n\n✏️ Course developed by @hayk.simonyan \n\n🔗 Presentation slides: https://www.notion.so/System-Design-Concepts-Course-and-Interview-Prep-Presentation-Slides-dd8abfd72e3e4b8eb3da402db13018cd\n\n⭐️ Contents ⭐️\n⌨️ (00:00) Introduction\n⌨️ (00:39) Computer Architecture (Disk Storage, RAM, Cache, CPU)\n⌨️ (04:22) Production App Architecture (CI/CD, Load Balancers, Logging & Monitoring)\n⌨️ (07:12) Design Requirements (CAP Theorem, Throughput, Latency, SLOs and SLAs)\n⌨️ (14:40) Networking (TCP, UDP, DNS, IP Addresses & IP Headers)\n⌨️ (19:03) Application Layer Protocols (HTTP, WebSockets, WebRTC, MQTT, etc)\n⌨️ (24:01) API Design\n⌨️ (29:19) Caching and CDNs\n⌨️ (36:33) Proxy Servers (Forward/Reverse Proxies)\n⌨️ (42:36) Load Balancers\n⌨️ (48:05) Databases (Sharding, Replication, ACID, Vertical & Horizontal Scaling)\n\n\n🎉 Thanks to our Champion and Sponsor supporters:\n👾 davthecoder\n👾 jedi-or-sith\n👾 南宮千影\n👾 Agustín Kussrow\n👾 Nattira Maneerat\n👾 Heather Wcislo\n👾 Serhiy Kalinets\n👾 Justin Hual\n👾 Otis Morgan \n👾 Oscar Rahnama\n\n--\n\nLearn to code for free and get a developer job: https://www.freecodecamp.org\n\nRead hundreds of articles on programming: https://freecodecamp.org/news",
      "title": "System Design Concepts Course and Interview Prep",
      "thumbnail_url": "https://i.ytimg.com/vi/F2FmTdLtb_4/hqdefault.jpg",
      "outline": null
    }
  ]
}
    const { data } = await apiClient.post('/recommend_videos', { messages });
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
