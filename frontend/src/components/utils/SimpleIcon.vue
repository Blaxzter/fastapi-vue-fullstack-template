<script lang="ts" setup>
defineProps({
  iconData: {
    type: Object,
    required: true,
  },
  className: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: 'currentColor',
  },
})
</script>

<template>
  <svg
    :class="className"
    role="img"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    :fill="color"
  >
    <path :d="iconData.path" />
    <title>{{ iconData.title }}</title>
  </svg>
</template>
