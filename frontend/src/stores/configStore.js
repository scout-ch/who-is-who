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
    initialize(config) {
      Object.keys(this.$state).forEach((key) => {
        if (key in config) {
          // deep copy
          this.$state[key] = JSON.parse(JSON.stringify(config[key]))
        }
      })
    },
    postConfig() {
      axios
        .post('/api/config', {
          data: this.$state,
        })
        .catch((err) => {
          console.error('Failed to post config: ', err)
        })
    },
    getField(fieldname) {
      // Get a reference to the field designated by fieldname.
      // Can be something like groups.exclude
      let field = this.$state
      fieldname.split('.').forEach((subfield) => {
        if (!(subfield in field)) {
          field[subfield] = {}
        }
        field = field[subfield]
      })
      return field
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
    isRoleExcluded(roleId) {
      return this.roles.exclude.includes(roleId)
    },
    excludeRole(roleId) {
      this.roles.exclude.push(roleId)
    },
    includeRole(roleId) {
      this.roles.exclude = this.roles.exclude.filter((e) => e != roleId)
    },
  },
})
