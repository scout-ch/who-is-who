import { defineStore } from 'pinia'
import axios from 'axios'

export const useConfigStore = defineStore('config', {
  state: () => ({
    groups: {
      exclude: [],
      description: {}, // groups.description[id] = { "de": "lorem ipsum...", "fr": "...", "it": "..." }
      name: {},
      order: {},
    },
    roles: {
      exclude: [],
      name: {}, // roles.overwritten[id] = { "de": "Mitglied", "fr": "Mèmbre", "it": "..." }
      order: {},
      tel: {},
      email: {},
    },
    images: {},
  }),
  actions: {
    theState() {
      return {
        groups: this.groups,
        roles: this.roles,
        images: this.images,
      }
    },
    loadConfig() {
      axios.get('/api/config').then((res) => {
        this.groups = res.data.groups
        this.roles = res.data.roles
        this.images = res.data.images
      }).catch((err) => {
        console.error('Failed to load config: ', err)
      })
    },
    postConfig() {
      axios.post('/api/config', {
        data: this.theState(),
      })
        .catch((err) => {
          console.error('Failed to post config: ', err)
        })
    },
    isGroupExcluded(groupId) {
      return this.groups.exclude.includes(groupId)
    },
    excludeGroup(groupId) {
      this.groups.exclude.push(groupId)
    },
    includeGroup(groupId) {
      this.groups.exclude = this.groups.exclude.filter((e) => e != groupId)
    },
    excludeRole(roleId) {
      this.roles.exclude.push(roleId)
    },
    includeRole(roleId) {
      this.roles.exclude = this.roles.exclude.filter((e) => e != roleId)
    },
  },
})
