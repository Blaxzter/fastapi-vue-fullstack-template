<script setup lang="ts">
import { useColorMode } from '@vueuse/core'

import logoBlack from '@/assets/logo/logo-no-background-black.svg'
import logoWhite from '@/assets/logo/logo-no-background-white.svg'

const mode = useColorMode()
</script>

<template>
  <img :src="mode === 'dark' ? logoWhite : logoBlack" alt="Logo" class="size-full" />
</template>
