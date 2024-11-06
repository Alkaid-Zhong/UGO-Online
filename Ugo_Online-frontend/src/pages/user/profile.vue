<template>
	<h1>{{ user.name }}</h1>
	<h1>{{ user.email }}</h1>
	<h1>{{ user.role }}</h1>
	<v-btn @click="logout()">Logout</v-btn>
</template>
<script setup>
import { user } from '@/store/user';
import { logout } from '@/api/user';
</script>