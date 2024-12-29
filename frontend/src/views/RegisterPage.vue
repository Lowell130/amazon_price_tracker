<template>
  <section class="bg-gray-50 dark:bg-gray-900">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0"
    >
      <div
        class="w-full bg-white rounded-lg shadow dark:border sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            Create a new account
          </h1>
          <form @submit.prevent="register" class="space-y-4 md:space-y-6">
            <div>
              <label
                for="username"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Username</label
              >
              <input
                v-model="username"
                id="username"
                type="text"
                placeholder="Your username"
                class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Email</label
              >
              <input
                v-model="email"
                id="email"
                type="email"
                placeholder="Your email"
                class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Password</label
              >
              <input
                v-model="password"
                id="password"
                type="password"
                placeholder="••••••••"
                autocomplete="new-password"
                class="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
              />

              <!-- Lista dei criteri dinamica -->
              <ul class="mt-2 text-sm text-gray-500">
                <li :class="getCriteriaClass(password.length >= 8)">
                  At least 8 characters
                </li>
                <li :class="getCriteriaClass(/[A-Z]/.test(password))">
                  An uppercase letter
                </li>
                <li :class="getCriteriaClass(/[a-z]/.test(password))">
                  A lowercase letter
                </li>
                <li :class="getCriteriaClass(/[0-9]/.test(password))">
                  A number
                </li>
                <li :class="getCriteriaClass(specialCharacterRegex.test(password))">
                  A special character
                </li>
              </ul>
            </div>

            <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>

            <button
              type="submit"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
            >
              Register
            </button>
            <p class="text-sm font-light text-gray-500 dark:text-gray-400">
              Already have an account?
              <router-link
                to="/login"
                class="font-medium text-primary-600 hover:underline dark:text-primary-500"
              >
                Sign in
              </router-link>
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      password: "",
      email: "",
      errorMessage: "",
      specialCharacterRegex: /[!@#$%^&*(),.?":{}|<>]/, // Aggiungi qui la regex
    };
  },
  methods: {
    getCriteriaClass(condition) {
      return condition ? "text-green-500" : "text-gray-500";
    },
    async register() {
      if (!this.validatePassword(this.password)) {
        this.errorMessage =
          "The password must include at least 8 characters, an uppercase letter, a lowercase letter, a number, and a special symbol like @ or #.";
        return;
      }

      try {
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            email: this.email,
          }),
        });

        if (response.ok) {
          this.$router.push("/login");
        } else {
          const data = await response.json();
          this.errorMessage = data.detail || "An error occurred.";
        }
      } catch (error) {
        console.error("Error during registration:", error);
        this.errorMessage = "An unexpected error occurred. Please try again.";
      }
    },
    validatePassword(password) {
      const minLength = 8;
      const hasUpperCase = /[A-Z]/.test(password);
      const hasLowerCase = /[a-z]/.test(password);
      const hasNumber = /[0-9]/.test(password);
      const hasSpecialChar = this.specialCharacterRegex.test(password);

      return (
        password.length >= minLength &&
        hasUpperCase &&
        hasLowerCase &&
        hasNumber &&
        hasSpecialChar
      );
    },
  },
};
</script>
