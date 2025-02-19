<script setup>
import { onMounted, ref } from "vue";

const container = ref(null);

const startJitsi = async () => {
  try {
    // Change these values to test different users:
    const payload = {
      name: "bobby",                   // For testing, try "Bobby" (disallowed) or "Alice" (allowed)
      email: "b@example.com",         // This email is NOT in ALLOWED_MODERATORS; try "alice@example.com" to allow
      room: "dynamic-room-123",
    };

    const response = await fetch("http://localhost:5001/generate-token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    // Check if the response is not OK (e.g., status 401)
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Backend error:", errorData.error);
      // Fall back to anonymous join if user is not allowed
      return joinAnonymously();
    }

    const data = await response.json();
    const jwtToken = data.token;

    if (!jwtToken) {
      console.error("Failed to get JWT");
      return joinAnonymously();
    }

    console.log("JWT received:", jwtToken);

    // Initialize Jitsi with the received JWT (authenticated, moderator privileges)
    new window.JitsiMeetExternalAPI("8x8.vc", {
      roomName:
        "vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/dynamic-room-123",
      parentNode: container.value,
      jwt: jwtToken,
    });
  } catch (error) {
    console.error("Error fetching JWT:", error);
    joinAnonymously();
  }
};

const joinAnonymously = () => {
  console.log("Joining anonymously (no moderator privileges).");
  new window.JitsiMeetExternalAPI("8x8.vc", {
    roomName:
      "vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/dynamic-room-123",
    parentNode: container.value,
  });
};

onMounted(() => {
  if (!window.JitsiMeetExternalAPI) {
    const script = document.createElement("script");
    script.src =
      "https://8x8.vc/vpaas-magic-cookie-90ee6c1a36b24c4396c110d15d7d80c3/external_api.js";
    script.async = true;
    script.onload = startJitsi;
    document.head.appendChild(script);
  } else {
    startJitsi();
  }
});
</script>

<template>
  <div ref="container" class="jaas-container"></div>
</template>

<style scoped>
.jaas-container {
  height: 100vh;
  width: 100%;
  min-width: 1200px; /* Adjust width as desired */
  margin: 0 auto;
  padding: 0;
}
</style>
