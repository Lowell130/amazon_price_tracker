<template>
   <section class="bg-blue-600 text-white">
    <div class="container mx-auto flex flex-col items-center justify-center py-16 px-6 text-center">
      <h1 class="text-4xl font-extrabold sm:text-6xl">
        Welcome to Our Platform
      </h1>
      <p class="mt-4 text-lg sm:text-xl">
        Discover a better way to manage your workflow and enhance productivity.
      </p>
      <div class="mt-6">
        <a href="#" class="bg-white text-blue-600 px-6 py-3 rounded-md font-medium shadow hover:bg-gray-100">
          Get Started
        </a>
        <a href="#" class="ml-4 text-white border border-white px-6 py-3 rounded-md hover:bg-blue-500">
          Learn More
        </a>
      </div>
    </div>


  <!-- Features Section -->
  
    <div class="container mx-auto px-6 py-16 bg-gray-50">
      <h2 class="text-center text-3xl font-bold text-gray-800 sm:text-4xl">
        Features You'll Love
      </h2>
      <p class="text-center text-gray-600 mt-4">
        Powerful tools designed to help you succeed.
      </p>

      <div class="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Feature 1 -->
        <div class="bg-white shadow rounded-lg p-6 text-center">
          <div class="bg-blue-100 text-blue-600 w-12 h-12 flex items-center justify-center mx-auto rounded-full mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2a4 4 0 10-2 0v2m0 4h6m6-10V7a2 2 0 00-2-2h-4M9 7h6m-2 4h2m4 0h2m-10 0h2M9 11H7" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-800">
            Feature One
          </h3>
          <p class="mt-2 text-gray-600">
            Detailed descriptions of the feature go here.
          </p>
        </div>

        <!-- Feature 2 -->
        <div class="bg-white shadow rounded-lg p-6 text-center">
          <div class="bg-blue-100 text-blue-600 w-12 h-12 flex items-center justify-center mx-auto rounded-full mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10l1-2h16l1 2M12 16V6m0 10h6m0 0H6m6-4h4" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-800">
            Feature Two
          </h3>
          <p class="mt-2 text-gray-600">
            Highlight another unique aspect here.
          </p>
        </div>

        <!-- Feature 3 -->
        <div class="bg-white shadow rounded-lg p-6 text-center">
          <div class="bg-blue-100 text-blue-600 w-12 h-12 flex items-center justify-center mx-auto rounded-full mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12v8m4-4H8m0 0h8m-4 0V8m0 0V4" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-800">
            Feature Three
          </h3>
          <p class="mt-2 text-gray-600">
            Add more information to help users understand.
          </p>
        </div>
      </div>
    </div>
  </section>
  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  