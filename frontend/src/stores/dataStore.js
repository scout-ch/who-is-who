import { defineStore } from 'pinia'

export const useDataStore = defineStore('data', {
  state: () => ({
    groups: {},
    roles: {},
    subgroups: {},
    rolesByGroups: {},
    images: {},
  }),
  actions: {
    initialize(data) {
      Object.keys(this.$state).forEach((key) => {
        if (key in data) {
          // deep copy
          this.$state[key] = JSON.parse(JSON.stringify(data[key]))
        }
      })
    },
  },
})
