<script setup>
import { onMounted, ref, reactive, nextTick } from 'vue';

const container = ref(null);
const showMeeting = ref(false);

// Reactive form data for login
const formData = reactive({
  name: '',
  email: '',
  room: 'dynamic-room-123'
});

// Function to start the Jitsi meeting with a JWT (authenticated, moderator privileges)
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

    // If the response isn't OK, log error and join anonymously.
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Backend error:", errorData.error);
      return joinAnonymously();
    }

    const data = await response.json();
    const jwtToken = data.token;

    if (!jwtToken) {
      console.error("Failed to get JWT");
      return joinAnonymously();
    }

    console.log("JWT received:", jwtToken);

    // Show the meeting container and wait for DOM update.
    showMeeting.value = true;
    await nextTick();

    // Initialize Jitsi with JWT (authenticated with moderator privileges).
    new window.JitsiMeetExternalAPI("8x8.vc", {
      roomName:
        "vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/" + formData.room,
      parentNode: container.value,
      jwt: jwtToken,
    });
  } catch (error) {
    console.error("Error fetching JWT:", error);
    joinAnonymously();
  }
};

// Fallback: join the meeting anonymously (without moderator privileges).
const joinAnonymously = async () => {
  console.log("Joining anonymously (no moderator privileges).");
  showMeeting.value = true;
  await nextTick();

  new window.JitsiMeetExternalAPI("8x8.vc", {
    roomName:
      "vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/" + formData.room,
    parentNode: container.value,
  });
};

// Handle form submission.
const handleSubmit = (e) => {
  e.preventDefault();
  startJitsi();
};

onMounted(() => {
  // Load the Jitsi external API script if not already loaded.
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
    <!-- Login form displayed before joining the meeting -->
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
          <input type="text" v-model="formData.room" id="room" required />
        </div>
        <button type="submit">Join Meeting</button>
      </form>
      <div class="anonymous-link">
        <a href="#" @click.prevent="joinAnonymously()">Join anonymously?</a>
      </div>
    </div>

    <!-- Jitsi container displayed after the meeting starts -->
    <div v-else ref="container" class="jaas-container"></div>
  </div>
</template>

<style scoped>
/* Full page container for centering content */
.page-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eef2f5;
  padding: 20px;
}

/* Styled login form */
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

/* Anonymous join link styling */
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

/* Jitsi container styling */
.jaas-container {
  height: 100vh;
  width: 100%;
  min-width: 1200px;
  margin: 0 auto;
  padding: 0;
}
</style>
