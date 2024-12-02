from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
  name: str
  email: str
  user_id: str

@dataclass
class Library:
  user_id: str
  video_id: Optional[str] = None  # URL can be inferred if needed

@dataclass
class Video:
  video_id: str
  url: str
  description: str
  title: str
  thumbnail_url: str
  outline: Optional[str] = None  # Outline might not always be present

@dataclass
class Quiz:
  video_id: str
  question: str
  answer: str
  qid: str

@dataclass
class Memory:
  mem_id: str  # Unique identifier for the memory
  memory: str  # The actual memory content
  user_id: str  # User ID to whom this memory belongs

# ===
# DB Functions
# ===
import os
import psycopg2
from psycopg2 import sql
from psycopg2.errors import UndefinedTable

# Connect to the database
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_DB = os.environ["PG_DB"]


def with_connection(func):
  """
  Function decorator for passing connections
  """

  def connection(*args, **kwargs):
    # Here, you may even use a connection pool
    conn = psycopg2.connect(dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
    try:
      rv = func(conn, *args, **kwargs)
    except Exception as e:
      conn.rollback()
      raise e
    else:
      # Can decide to see if you need to commit the transaction or not
      conn.commit()
    finally:
      conn.close()
    return rv

  return connection

@with_connection
def create_tables(conn):
  cur = conn.cursor()
  query = '''
-- User Table
CREATE TABLE IF NOT EXISTS Users (
  user_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);

-- Video Table
CREATE TABLE IF NOT EXISTS Video (
  video_id TEXT PRIMARY KEY,
  url TEXT NOT NULL,
  description TEXT NOT NULL,
  title TEXT NOT NULL,
  thumbnail_url TEXT NOT NULL,
  outline TEXT
);

-- Library Table
CREATE TABLE IF NOT EXISTS Library (
  user_id TEXT NOT NULL REFERENCES Users(user_id),
  video_id TEXT NOT NULL REFERENCES Video(video_id),
  PRIMARY KEY (user_id, video_id)
);

-- Quiz Table
CREATE TABLE IF NOT EXISTS Quiz (
  qid TEXT PRIMARY KEY,
  video_id TEXT NOT NULL REFERENCES Video(video_id),
  question TEXT NOT NULL,
  answer TEXT NOT NULL
);

-- Memory Table
CREATE TABLE IF NOT EXISTS Memory (
  mem_id TEXT PRIMARY KEY,
  memory TEXT NOT NULL,
  user_id TEXT NOT NULL REFERENCES Users(user_id)
);
  '''
  cur.execute(query)
  cur.close()

@with_connection
def check_and_create_tables(conn):
    required_tables = ["users", "video", "library", "memory", "quiz"]
    for table in required_tables:
        try:
            with conn.cursor() as cur:
                cur.execute(f"SELECT 1 FROM {table} LIMIT 1")
        except UndefinedTable:
            print(f"Table {table} is missing. Creating tables...")
            create_tables()  # Call to create tables if any are missing
            break

# ===
# Users
# ===
@with_connection
def create_user(conn, user: User):
  insert_query = """
  INSERT INTO Users (user_id, name, email) VALUES (%s, %s, %s)
  """
  with conn.cursor() as cur:
    cur.execute(insert_query, (user.user_id, user.name, user.email))


@with_connection
def read_user(conn, user_id: str) -> Optional[User]:
  select_query = """
  SELECT user_id, name, email FROM Users WHERE user_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (user_id,))
    result = cur.fetchone()
    return User(*result) if result else None


@with_connection
def update_user(conn, user_id: str, user: User):
  update_query = """
  UPDATE Users SET name = %s, email = %s WHERE user_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(update_query, (user.name, user.email, user_id))


@with_connection
def delete_user(conn, user_id: str):
  delete_query = """
  DELETE FROM Users WHERE user_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(delete_query, (user_id,))

@with_connection
def check_user_by_email(conn, email: str) -> bool:
  """
  Checks if a user with the given email exists.

  :param conn: Database connection
  :param email: Email address to check
  :return: True if the user exists, False otherwise
  """
  select_query = """
  SELECT EXISTS (
    SELECT 1 
    FROM Users 
    WHERE email = %s
  )
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (email,))
    exists = cur.fetchone()[0]
    return exists

# ===
# Videos
# ===
@with_connection
def create_video(conn, video: Video):
  insert_query = """
  INSERT INTO Video (video_id, url, description, title, thumbnail_url, outline) VALUES (%s, %s, %s, %s, %s, %s)
  """
  with conn.cursor() as cur:
    cur.execute(insert_query, (video.video_id, video.url, video.description, video.title, video.thumbnail_url, video.outline))


@with_connection
def read_video(conn, video_id: str) -> Optional[Video]:
  select_query = """
  SELECT video_id, url, description, title, thumbnail_url, outline FROM Video WHERE video_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (video_id,))
    result = cur.fetchone()
    return Video(*result) if result else None


@with_connection
def update_video(conn, video_id: str, video: Video):
  update_query = """
  UPDATE Video SET url = %s, description = %s, title = %s, thumbnail_url = %s, outline = %s WHERE video_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(update_query, (video.url, video.description, video.title, video.thumbnail_url, video.outline, video_id))


@with_connection
def delete_video(conn, video_id: str):
  delete_query = """
  DELETE FROM Video WHERE video_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(delete_query, (video_id,))

@with_connection
def get_videos_by_user(conn, user_id: str) -> List[Video]:
  """
  Retrieves all videos in the library for a specific user.

  :param conn: Database connection
  :param user_id: User ID whose library videos are to be retrieved
  :return: List of Video objects
  """
  select_query = """
  SELECT v.video_id, v.url, v.description, v.title, v.thumbnail_url, v.outline
  FROM Library l
  JOIN Video v ON l.video_id = v.video_id
  WHERE l.user_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (user_id,))
    results = cur.fetchall()
    return [Video(video_id=row[0], url=row[1], description=row[2], title=row[3], thumbnail_url=row[4], outline=row[5]) for row in results]

# ===
# Library
# ===
@with_connection
def create_library(conn, library: Library):
  insert_query = """
  INSERT INTO Library (user_id, video_id) VALUES (%s, %s)
  """
  with conn.cursor() as cur:
    cur.execute(insert_query, (library.user_id, library.video_id))


@with_connection
def read_library(conn, user_id: str, video_id: Optional[str] = None):
  select_query = """
  SELECT user_id, video_id FROM Library WHERE user_id = %s AND (video_id = %s OR %s IS NULL)
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (user_id, video_id, video_id))
    return cur.fetchall()


@with_connection
def delete_library(conn, user_id: str, video_id: Optional[str] = None):
  delete_query = """
  DELETE FROM Library WHERE user_id = %s AND (video_id = %s OR %s IS NULL)
  """
  with conn.cursor() as cur:
    cur.execute(delete_query, (user_id, video_id, video_id))

@with_connection
def check_video_in_library(conn, user_id: str, video_id: str) -> bool:
  """
  Checks if a video is in the user's library.

  :param conn: Database connection
  :param user_id: User ID
  :param video_id: Video ID
  :return: True if the video is in the user's library, False otherwise
  """
  select_query = """
  SELECT EXISTS (
    SELECT 1 
    FROM Library 
    WHERE user_id = %s AND video_id = %s
  )
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (user_id, video_id))
    exists = cur.fetchone()[0]
    return exists

# ===
# Quiz
# ===
@with_connection
def create_quiz(conn, quiz: Quiz):
  insert_query = """
  INSERT INTO Quiz (qid, video_id, question, answer) VALUES (%s, %s, %s, %s)
  """
  with conn.cursor() as cur:
    cur.execute(insert_query, (quiz.qid, quiz.video_id, quiz.question, quiz.answer))


@with_connection
def read_quiz(conn, qid: str) -> Optional[Quiz]:
  select_query = """
  SELECT qid, video_id, question, answer FROM Quiz WHERE qid = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (qid,))
    result = cur.fetchone()
    return Quiz(*result) if result else None


@with_connection
def update_quiz(conn, qid: str, quiz: Quiz):
  update_query = """
  UPDATE Quiz SET video_id = %s, question = %s, answer = %s WHERE qid = %s
  """
  with conn.cursor() as cur:
    cur.execute(update_query, (quiz.video_id, quiz.question, quiz.answer, qid))


@with_connection
def delete_quiz(conn, qid: str):
  delete_query = """
  DELETE FROM Quiz WHERE qid = %s
  """
  with conn.cursor() as cur:
    cur.execute(delete_query, (qid,))

@with_connection
def read_quizzes_by_video(conn, video_id: str) -> List[Quiz]:
  """
  Reads all quiz questions and answers for a specific video.

  :param conn: Database connection
  :param video_id: Video ID whose quizzes are to be retrieved
  :return: List of Quiz objects
  """
  select_query = """
  SELECT qid, video_id, question, answer
  FROM Quiz
  WHERE video_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (video_id,))
    results = cur.fetchall()
    return [Quiz(qid=row[0], video_id=row[1], question=row[2], answer=row[3]) for row in results]

# ===
# Memory
# ===
@with_connection
def create_memory(conn, memory: Memory):
  insert_query = """
  INSERT INTO Memory (mem_id, memory, user_id) VALUES (%s, %s, %s)
  """
  with conn.cursor() as cur:
    cur.execute(insert_query, (memory.mem_id, memory.memory, memory.user_id))


@with_connection
def read_memory(conn, mem_id: str) -> Optional[Memory]:
  select_query = """
  SELECT mem_id, memory, user_id FROM Memory WHERE mem_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (mem_id,))
    result = cur.fetchone()
    return Memory(result[0], result[1], result[2]) if result else None


@with_connection
def update_memory(conn, mem_id: str, memory: Memory):
  update_query = """
  UPDATE Memory SET memory = %s, user_id = %s WHERE mem_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(update_query, (memory.memory, memory.user_id, mem_id))


@with_connection
def delete_memory(conn, mem_id: str):
  delete_query = """
  DELETE FROM Memory WHERE mem_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(delete_query, (mem_id,))

@with_connection
def read_memories_by_user(conn, user_id: str) -> List[Memory]:
  """
  Reads all memories for a specific user.

  :param conn: Database connection
  :param user_id: User ID whose memories are to be retrieved
  :return: List of Memory objects
  """
  select_query = """
  SELECT mem_id, memory, user_id
  FROM Memory
  WHERE user_id = %s
  """
  with conn.cursor() as cur:
    cur.execute(select_query, (user_id,))
    results = cur.fetchall()
    return [Memory(mem_id=row[0], memory=row[1], user_id=row[2]) for row in results]

