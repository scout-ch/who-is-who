<script setup>
import Groups from '@/components/group/Groups.vue'
import Generator from '@/components/Generator.vue'
</script>

<template>
  <main class="h-full m-auto">
    <div class="flex justify-center gap-3 w-5/6 m-auto mt-1">
      <Groups class="w-full min-w-2xl" />
      <Generator class="w-full" />
    </div>
  </main>
</template>
