<template>
  <router-view />
</template>

<script>
export default {
  methods: {
    async startSession() {
      if (!this.$session.exists) {
        this.$session.start();
      }
    },
  },
};
</script>
