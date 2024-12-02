import { useState, useRef, useEffect } from 'react'
import { login, getProfile, logout, recommendVideos } from '@/api.js'

function App() {
  const [profile, setProfile] = useState(undefined)
  const [messages, setMessages] = useState(undefined)
  const [query, setQuery] = useState('Lets learn rust today');
  const [pressedSearch, setPressedSearch] = useState(false);
  const [recommendedVideos, setRecommendedVideos] = useState(undefined);

  useEffect(() => {
    setMessages(
      [
        {
          "role": "user",
          "content": "i want to learn rust"
        },
        {
          "role": "assistant",
          "content": "Based on your query and the recommended videos, it seems you're a complete beginner to Rust.  The videos are well-suited to your current level.\n\n* **\"Rust Programming Course for Beginners - Tutorial\"**: This is an excellent starting point. It covers fundamental concepts through practical examples, building small projects.  This is ideal if you learn best by doing.\n\n* **\"Learn Rust Programming - Complete Course 💻\"**: This video offers a more theoretical approach, covering a broader range of topics in greater depth.  While it's comprehensive, it might be overwhelming if you haven't grasped the basics yet.  It's best approached *after* a foundational course like the first one.\n\n* **\"Rust Project Tutorial – Authentication Server Using Warp + JWT\"**: This is a project-based course that requires a solid understanding of Rust's core concepts.  Jumping into this without prior knowledge would be very challenging.  This is a great follow-up once you've mastered the fundamentals from the other two.\n\n**Recommendation:** Start with the \"Rust Programming Course for Beginners - Tutorial\".  Once you've completed it and feel comfortable with the basics (variables, data types, functions, control flow, ownership, borrowing), you can then decide whether you want a more theoretical deep dive (\"Learn Rust Programming - Complete Course\") before tackling a larger project like the authentication server.  Trying the project-based course too early could be frustrating.\n"
        },
        {
          "role": "user",
          "content": "but remember that I have a decade worth of experience in software engineering including system programming and website building, albiet in different language."
        },
  {
    "role": "assistant",
    "content": "Given your decade of experience in software engineering, including system programming and web development,  the beginner-level Rust tutorials are likely unnecessary.  Jumping straight into the \"Learn Rust Programming - Complete Course\" is a viable option.  Its comprehensive nature will cover the fundamentals efficiently, leveraging your existing programming knowledge.\n\nThe course covers a wide range of topics including ownership, borrowing, and advanced concepts like lifetimes and iterators.  These are areas where your prior experience might not fully translate, and the video's structured approach will be beneficial.\n\nThe \"Rust Project Tutorial – Authentication Server Using Warp + JWT\" is best left for after you've solidified your understanding from the complete course.  While you could potentially attempt it now, the learning curve could be steeper than expected, potentially leading to frustration.  Completing the \"Learn Rust Programming - Complete Course\" first ensures you possess the necessary foundational skills for this project.\n\nThe \"System Design Concepts Course and Interview Prep\" is entirely separate.  It focuses on system architecture, not Rust itself.  While relevant to your broader career goals, it shouldn't be prioritized before gaining fluency in Rust's core features. You can consider this course once you feel confident working with Rust on smaller to medium sized projects.\n\n**Recommendation:** Begin with \"Learn Rust Programming - Complete Course\".  Use it as a deep dive to master Rust's unique features.  Once finished,  move onto the authentication server project. The system design course can be pursued concurrently or later, depending on your career priorities.\n"
  }
      ]
    )
  setRecommendedVideos(
    [
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
  )
  }, [])

  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const response = await getProfile();
        if (response && response.response) {
          console.log(response.response)
          setProfile(response.response);
        } else {
          setProfile(undefined);
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        setProfile(undefined);
      }
    };

    checkAuthentication();
  }, []);

  function handleLogout() {
    logout().then(setProfile(undefined))
  }

  const queryRef = useRef(null);
  const updateQuery = () => {
    const query = queryRef.current?.value || '';
    setQuery(query);
  };
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') { 
      setPressedSearch(true)
    }
  };

  useEffect(() => {
    if (pressedSearch && query){
      setMessages(prevMessages => {
        let to_send_messages;
        if (prevMessages == undefined) {
          to_send_messages = [
            {role: 'user', content: query},
          ]
        } else {
          to_send_messages = [...prevMessages, {role: 'user', content: query}]
        }
        const {reply, videos} = recommendVideos(to_send_messages)
        setRecommendedVideos(videos)
        setQuery('')
        return [...to_send_messages, reply]
      })
      setPressedSearch(false)
    }
  }, [pressedSearch])

  return (
    <div className="flex flex-col h-screen">
      <nav className="bg-gray-800 p-4">
        <div className="flex justify-between items-center">
          <h1 className="text-white text-2xl font-bold">AI Learning Assistant</h1>
          <div>
            {profile !== undefined && (
              <>
                <button className="btn btn-ghost text-white mr-4">Library</button>
                <button className="btn btn-ghost text-white" onClick={handleLogout}>Logout</button>
              </>
            )}
          </div>
        </div>
      </nav>

      <div className="flex-grow">
        {profile === undefined && (
          <div className="h-full flex items-center justify-center">
            <button className="btn" onClick={() => login()}>Login</button>
          </div>
        )}

        {messages === undefined && profile !== undefined && (
          <div className='h-full flex flex-col items-center justify-center'>
            <div className='text-3xl'>What do you want to learn today?</div>
            <input type="text" placeholder="I want to learn Go" className="input input-bordered w-6/12 mt-5" ref={queryRef} value={query} onChange={updateQuery} onKeyPress={handleKeyPress} />
          </div>
        )}

        {messages !== undefined && (
          <div className="chat-container w-full h-full">
            <div className='grid grid-cols-12 gap-4 h-full'>
              <div className='col-span-6 p-4'>
                {messages.map((message, index) => (
                  <div key={index} className={`chat ${message.role === 'user' ? 'chat-end' : 'chat-start'} mb-4`}>
                    <div className={`chat-bubble ${message.role === 'user' ? 'bg-slate-200' : 'bg-slate-500'}`}>
                      {message.content}
                    </div>
                  </div>
                ))}
                <div className="mt-4">
                  <input
                    type="text"
                    placeholder="Type your message..."
                    className="input input-bordered w-9/12"
                    ref={queryRef}
                    value={query}
                    onChange={updateQuery}
                    onKeyPress={handleKeyPress}
                  />
                  <button className='btn ml-2' onClick={() => setPressedSearch(true)}>Send</button>
                </div>
              </div>
              <div className='col-span-6 p-4 grid grid-cols-2 grid-rows-2 h-svh gap-4'>
                {recommendedVideos && recommendedVideos.map((video, index) => (
                  <div key={index} className="mb-4">
                    <img src={video.thumbnail_url} alt={video.title} className="w-full mb-2" />
                    <h3 className="text-lg font-semibold truncate">{video.title}</h3>
                    <p className="text-sm truncate">{video.description.substring(0, 100)}...</p>
                    <a href={video.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">Watch Video</a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
