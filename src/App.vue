<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div>
    <JitsiMeet />
  </div>
</template>

<script>
import JitsiMeet from "./components/jitsoMeet.vue";

export default {
  components: {
    JitsiMeet,
  },
};
</script>


