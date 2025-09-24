import { defineStore } from 'pinia'

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
    },
  }),
  actions: {
    excludeGroup(groupId) {
      this.groups.exclude.push(groupId)
    },
    includeGroup(groupId) {
      this.groups.exclude = this.groups.exclude.filter((e) => e != groupId)
    },
    exludeRole(roleId) {
      this.roles.exclude.push(roleId)
    },
    includeRole(roleId) {
      this.roles.exclude = this.roles.exclude.filter((e) => e != roleId)
    },
  },
})
