<script setup>
import { onMounted, ref, reactive, nextTick } from 'vue';

const container = ref(null);
const showMeeting = ref(false);

// Reactive form data for login
const formData = reactive({
  name: '',
  email: '',
  room: ''
});

// Function to start the Jitsi meeting as an authenticated user (JWT with moderator privileges)
const startJitsi = async () => {
  try {
    const payload = {
      name: formData.name,
      email: formData.email,
      room: formData.room,
    };

    const response = await fetch("http://localhost:5001/generate-token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Backend error:", errorData.error);
      alert(errorData.error);
      return; // Do not join the meeting
    }

    const data = await response.json();
    const jwtToken = data.token;

    if (!jwtToken) {
      console.error("Failed to get JWT");
      alert("Failed to get JWT. Please try again later.");
      return;
    }

    console.log("JWT received:", jwtToken);

    showMeeting.value = true;
    await nextTick();

    new window.JitsiMeetExternalAPI("8x8.vc", {
      roomName:
        "vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/" + formData.room,
      parentNode: container.value,
      jwt: jwtToken,
    });
  } catch (error) {
    console.error("Error fetching JWT:", error);
    alert("An unexpected error occurred. Please try again.");
  }
};

// Function to join anonymously (without moderator privileges).
const joinAnonymously = async () => {
  // Ensure room name is provided. If not, prompt for one.
  if (!formData.room.trim()) {
    const userRoom = prompt("Please enter the room name you want to join:");
    if (userRoom && userRoom.trim()) {
      formData.room = userRoom.trim();
    } else {
      alert("Room name is required to join anonymously.");
      return;
    }
  }
  // Use dummy values for name and email for anonymous join.
  const payload = {
    name: "Anonymous",
    email: "anonymous@example.com",
    room: formData.room,
  };

  try {
    const response = await fetch("http://localhost:5001/generate-token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Backend error:", errorData.error);
      alert(errorData.error);
      return;
    }

    const data = await response.json();
    const jwtToken = data.token;
    if (!jwtToken) {
      alert("Failed to get token. Please try again.");
      return;
    }

    console.log("JWT received (anonymous):", jwtToken);

    showMeeting.value = true;
    await nextTick();

    new window.JitsiMeetExternalAPI("8x8.vc", {
      roomName:
        "vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/" + formData.room,
      parentNode: container.value,
      jwt: jwtToken,
    });
  } catch (error) {
    console.error("Error joining anonymously:", error);
    alert("An error occurred. Please try again.");
  }
};

// Handle form submission for authenticated join.
const handleSubmit = (e) => {
  e.preventDefault();
  // If room is empty, generate a default room name
  if (!formData.room.trim()) {
    formData.room = 'room-' + Math.random().toString(36).substring(2, 10);
  }
  startJitsi();
};

onMounted(() => {
  if (!window.JitsiMeetExternalAPI) {
    const script = document.createElement("script");
    script.src =
      "https://8x8.vc/vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/external_api.js";
    script.async = true;
    script.onload = () => console.log("Jitsi external API loaded.");
    document.head.appendChild(script);
  }
});
</script>

<template>
  <div class="page-container">
    <div v-if="!showMeeting" class="login-form">
      <h2>Join Meeting</h2>
      <form @submit="handleSubmit">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" v-model="formData.name" id="name" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="formData.email" id="email" required />
        </div>
        <div class="form-group">
          <label for="room">Room:</label>
          <input type="text" v-model="formData.room" id="room" placeholder="Enter room name" required />
        </div>
        <button type="submit">Join Meeting as Authenticated User</button>
      </form>
      <div class="anonymous-link">
        <a href="#" @click.prevent="joinAnonymously()">Join anonymously?</a>
      </div>
    </div>
    <div v-else ref="container" class="jaas-container"></div>
  </div>
</template>

<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eef2f5;
  padding: 20px;
}

.login-form {
  background: #ffffff;
  padding: 30px 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 400px;
  text-align: center;
}

.login-form h2 {
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.login-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #555;
}

.login-form input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.login-form button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 4px;
  background: #007bff;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
}

.login-form button:hover {
  background: #0056b3;
}

.anonymous-link {
  margin-top: 15px;
  font-size: 0.9rem;
}

.anonymous-link a {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
}

.anonymous-link a:hover {
  text-decoration: underline;
}

.jaas-container {
  height: 100vh;
  width: 100%;
  min-width: 1200px;
  margin: 0 auto;
  padding: 0;
}
</style>
