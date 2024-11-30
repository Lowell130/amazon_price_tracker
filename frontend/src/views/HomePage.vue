<template>

<div class="bg-gray-50 text-gray-800">

 

  <!-- Hero Section -->
  <section class="bg-indigo-600 text-white">
    <div class="container mx-auto px-6 py-16 text-center">
      <h2 class="text-4xl font-bold">Track Amazon Prices Effortlessly</h2>
      <p class="mt-4 text-lg">Subscribe, add products, and monitor prices to save money and get the best deals!</p>
      <a href="#subscribe" class="mt-6 inline-block bg-white text-indigo-600 font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-gray-100">Get Started</a>
    </div>
  </section>

  <!-- Features Section -->
  <section id="features" class="py-12 bg-gray-100">
    <div class="container mx-auto px-6">
      <h3 class="text-3xl font-bold text-center text-gray-800">How It Works</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
        <!-- Feature 1 -->
        <div class="bg-white shadow-md rounded-lg p-6">
          <div class="flex items-center justify-center h-16 w-16 bg-indigo-100 rounded-full mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 0c-4 0-8 2-8 6v3h16v-3c0-4-4-6-8-6z" />
            </svg>
          </div>
          <h4 class="text-xl font-bold text-center text-gray-800">Create an Account</h4>
          <p class="text-center text-gray-600 mt-2">Sign up to start tracking prices and receive alerts.</p>
        </div>
        <!-- Feature 2 -->
        <div class="bg-white shadow-md rounded-lg p-6">
          <div class="flex items-center justify-center h-16 w-16 bg-indigo-100 rounded-full mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </div>
          <h4 class="text-xl font-bold text-center text-gray-800">Add Products</h4>
          <p class="text-center text-gray-600 mt-2">Enter the Amazon links of the products you want to monitor.</p>
        </div>
        <!-- Feature 3 -->
        <div class="bg-white shadow-md rounded-lg p-6">
          <div class="flex items-center justify-center h-16 w-16 bg-indigo-100 rounded-full mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m-9 4h12m-6-4h6m-6-16h6m-9 4h12m-9 0h9m0-4h-6" />
            </svg>
          </div>
          <h4 class="text-xl font-bold text-center text-gray-800">Monitor Prices</h4>
          <p class="text-center text-gray-600 mt-2">Get instant notifications when prices drop to your target range.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Subscription Section -->
  <section id="subscribe" class="py-16 bg-white">
    <div class="container mx-auto px-6 text-center">
      <h3 class="text-3xl font-bold text-gray-800">Subscribe Now</h3>
      <p class="mt-4 text-gray-600">Start tracking your favorite products on Amazon today.</p>
      <form class="mt-8 flex flex-col md:flex-row items-center justify-center gap-4">
        <input type="email" placeholder="Enter your email" class="w-full md:w-1/3 px-4 py-3 rounded-lg shadow-md border border-gray-300 focus:ring-2 focus:ring-indigo-600">
        <button type="submit" class="bg-indigo-600 text-white px-6 py-3 rounded-lg shadow-md hover:bg-indigo-700">Subscribe</button>
      </form>
    </div>
  </section>

 


</div>

  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  