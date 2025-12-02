<template>
  <section class="bg-gray-50 dark:bg-gray-900">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <!-- <a href="#" class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
        <img class="w-8 h-8 mr-2" src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/logo.svg" alt="logo">
        MyApp
      </a> -->
      <div class="w-full p-6 bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md dark:bg-gray-800 dark:border-gray-700 sm:p-8">
        <h2 class="mb-1 text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
          Reset Your Password
        </h2>
        <form @submit.prevent="resetPassword" class="mt-4 space-y-4 lg:mt-5 md:space-y-5">
          <div>
            <label for="token" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Reset Token</label>
            <input
              type="text"
              id="token"
              v-model="token"
              readonly
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              required
            />
          </div>
          <div>
            <label for="newPassword" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">New Password</label>
            <input
              type="password"
              id="newPassword"
              v-model="newPassword"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
          >
            Change Password
          </button>
        </form>
        <p v-if="message" class="mt-4 text-sm font-medium text-green-500">{{ message }}</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      token: '',
      newPassword: '',
      message: ''
    };
  },
  created() {
    // Estrai il token dalla query string
    const urlParams = new URLSearchParams(window.location.search);
    this.token = urlParams.get('token');
  },
  methods: {
    async resetPassword() {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/auth/reset-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token: this.token, new_password: this.newPassword })
        });

        const data = await response.json();
        this.message = data.message;
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
};
</script>
