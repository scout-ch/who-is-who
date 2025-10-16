<template>
  <div class="loading-overlay">
    <div class="spinner" />
  </div>
</template>

<style scoped>
.loading-overlay {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #ccc;
  border-top-color: #42b983;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
