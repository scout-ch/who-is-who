<script setup>
import { ref } from 'vue'
import Group from './Group.vue'

const root_group = '2'
</script>

<template>
  <div>
    <Group :groupId="root_group" :expanded="true" />
  </div>
</template>
