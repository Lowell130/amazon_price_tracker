<template>
  <header class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 px-4 md:px-8 py-4" :class="{ 'py-2': isScrolled }">
    <!-- Navbar Container (Floating Glassmorphism) -->
    <nav 
      class="max-w-7xl mx-auto rounded-2xl border border-white/20 bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl shadow-lg transition-all duration-300"
      :class="{ 'shadow-xl border-white/30': isScrolled }"
    >
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          
          <!-- Logo & Brand -->
          <router-link to="/" class="flex items-center group space-x-2">
            <div class="p-2 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 shadow-md group-hover:scale-110 transition-transform duration-300">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
              PriceHub.it
            </span>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-1">
            <!-- Main Group: Public & Core Tracking -->
            <router-link to="/" class="flex items-center px-4 py-2 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/50 dark:hover:bg-blue-900/20 transition-all duration-300 group">
              <svg class="w-4 h-4 mr-2 opacity-70 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
              Home
            </router-link>

            <router-link to="/blog" class="flex items-center px-4 py-2 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/50 dark:hover:bg-blue-900/20 transition-all duration-300 group">
              <svg class="w-4 h-4 mr-2 opacity-70 group-hover:rotate-12 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10l4 4v10a2 2 0 01-2 2zM14 4v4h4"/></svg>
              Blog
            </router-link>

            <template v-if="isAuthenticated">
              <div class="h-6 w-px bg-gray-200 dark:bg-gray-700 mx-2"></div>
              
              <router-link to="/dashboard" class="flex items-center px-4 py-2 rounded-xl text-sm font-black text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/50 dark:hover:bg-blue-900/30 transition-all duration-300">
                <svg class="w-4 h-4 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                Dashboard
              </router-link>
              
              <router-link to="/analysis" class="flex items-center px-4 py-2 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50/50 dark:hover:bg-blue-900/20 transition-all duration-300 group">
                <svg class="w-4 h-4 mr-2 text-purple-500 group-hover:animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
                AI Insights
              </router-link>

              <!-- Gestione Dropdown (Admin) -->
              <div v-if="isAdmin" class="relative group" @mouseenter="clearCloseTimeout('admin'); isAdminDropdownOpen = true" @mouseleave="closeWithDelay('admin')">
                <button class="flex items-center px-4 py-2 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:bg-gray-100/50 dark:hover:bg-gray-800/50 transition-all h-full">
                  <svg class="w-4 h-4 mr-2 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  Gestione
                  <svg class="w-4 h-4 ml-1 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7"/></svg>
                </button>
                <div v-show="isAdminDropdownOpen" class="absolute left-0 mt-0 pt-2 w-48 bg-transparent z-50">
                  <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-700 py-2 animate-fadeIn">
                    <router-link to="/admin/users" class="flex items-center px-4 py-2.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400">
                      <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                      Utenti
                    </router-link>
                    <router-link to="/admin/articles" class="flex items-center px-4 py-2.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400">
                      <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10l4 4v10a2 2 0 01-2 2zM14 4v4h4"/></svg>
                      Articoli AI
                    </router-link>
                    <router-link to="/admin/analytics" class="flex items-center px-4 py-2.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400">
                      <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                      Analytics
                    </router-link>
                    <router-link to="/admin/settings" class="flex items-center px-4 py-2.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400 border-t border-gray-50 dark:border-gray-700 mt-1 pt-3">
                      <svg class="w-4 h-4 mr-3 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 0 0-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 0 0-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 0 0-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 0 0-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 0 0 1.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      Impostazioni
                    </router-link>
                  </div>
                </div>
              </div>

              <!-- Spacer for Account -->
              <div class="flex-grow"></div>

              <!-- Account Dropdown -->
              <div class="relative group ml-4" @mouseenter="clearCloseTimeout('account'); isAccountDropdownOpen = true" @mouseleave="closeWithDelay('account')">
                <button class="flex items-center px-4 py-2 rounded-2xl bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 text-sm font-black text-gray-900 dark:text-white shadow-sm hover:shadow-md transition-all h-full">
                  <div class="w-7 h-7 bg-blue-500 rounded-full flex items-center justify-center text-white mr-2 text-[10px] font-black uppercase">
                    {{ getInitials() }}
                  </div>
                  Account
                  <svg class="w-4 h-4 ml-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7"/></svg>
                </button>
                <div v-show="isAccountDropdownOpen" class="absolute right-0 mt-0 pt-2 w-56 bg-transparent z-50">
                  <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-100 dark:border-gray-700 py-2 animate-fadeIn overflow-hidden">
                    <router-link to="/profile" class="flex items-center px-4 py-3 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-900/50">
                      <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                      Il mio Profilo
                    </router-link>
                    <a :href="externalLink('/extension-download')" class="flex items-center px-4 py-3 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-900/50">
                      <svg class="w-4 h-4 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                      Scarica Estensione
                    </a>
                    <div class="h-px bg-gray-100 dark:bg-gray-700 my-1"></div>
                    <button @click="logout" class="w-full flex items-center px-4 py-3 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20">
                      <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                      Disconnetti
                    </button>
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <div class="flex items-center space-x-2 ml-4">
                <router-link to="/login" class="px-5 py-2 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:text-blue-600 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all">
                  Accedi
                </router-link>
                <router-link to="/register" class="px-6 py-2.5 rounded-xl bg-blue-600 text-white text-sm font-black shadow-lg shadow-blue-500/20 hover:bg-blue-700 hover:scale-105 transition-all">
                  Registrati Gratis
                </router-link>
              </div>
            </template>
          </div>

          <!-- Mobile Menu Button -->
          <div class="md:hidden flex items-center">
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen"
              class="p-2 rounded-xl text-gray-600 dark:text-gray-300 bg-gray-100/50 dark:bg-gray-800/50 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors shadow-sm"
            >
              <svg v-if="!isMobileMenuOpen" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" /></svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation Enhancements -->
      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform -translate-y-4 opacity-0 scale-95"
        enter-to-class="transform translate-y-0 opacity-100 scale-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform translate-y-0 opacity-100 scale-100"
        leave-to-class="transform -translate-y-4 opacity-0 scale-95"
      >
        <div v-if="isMobileMenuOpen" class="md:hidden border-t border-gray-100 dark:border-gray-800 overflow-y-auto max-h-[80vh] bg-white/95 dark:bg-gray-900/95 backdrop-blur-3xl rounded-b-2xl shadow-2xl">
          <div class="px-6 py-8 space-y-6">
            <!-- Core Navigation -->
            <div class="space-y-4">
              <p class="text-[10px] font-black uppercase text-gray-400 tracking-widest pl-2">Menu Principale</p>
              <router-link to="/" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                <svg class="w-5 h-5 mr-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg> Home
              </router-link>
              <router-link to="/blog" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                <svg class="w-5 h-5 mr-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10l4 4v10a2 2 0 01-2 2zM14 4v4h4"/></svg> Blog
              </router-link>
            </div>

            <template v-if="isAuthenticated">
              <div class="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-800">
                <p class="text-[10px] font-black uppercase text-gray-400 tracking-widest pl-2">Strumenti</p>
                <router-link to="/dashboard" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-black text-blue-600 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/30">
                  <svg class="w-5 h-5 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg> Dashboard
                </router-link>
                <router-link to="/analysis" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  <svg class="w-5 h-5 mr-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg> AI Insights
                </router-link>
              </div>

              <div v-if="isAdmin" class="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-800">
                <p class="text-[10px] font-black uppercase text-amber-500 tracking-widest pl-2">Admin Management</p>
                <router-link to="/admin/users" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white">
                  <svg class="w-5 h-5 mr-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg> Utenti
                </router-link>
                <router-link to="/admin/articles" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white">
                  <svg class="w-5 h-5 mr-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10l4 4v10a2 2 0 01-2 2zM14 4v4h4"/></svg> Articoli AI
                </router-link>
                <router-link to="/admin/analytics" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white">
                  <svg class="w-5 h-5 mr-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg> Analytics
                </router-link>
              </div>

              <div class="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-800">
                <router-link to="/profile" @click="isMobileMenuOpen = false" class="flex items-center p-3 rounded-2xl text-lg font-bold text-gray-900 dark:text-white">
                  <svg class="w-5 h-5 mr-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg> Il mio Profilo
                </router-link>
                <button @click="logout(); isMobileMenuOpen = false" class="w-full flex items-center p-3 rounded-2xl text-lg font-bold text-red-600 bg-red-50 dark:bg-red-900/10">
                  <svg class="w-5 h-5 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg> Logout
                </button>
              </div>
            </template>
            <template v-else>
              <div class="pt-6 space-y-4">
                <router-link to="/login" @click="isMobileMenuOpen = false" class="block w-full text-center py-4 rounded-2xl bg-gray-100 dark:bg-gray-800 text-lg font-bold text-gray-900 dark:text-white transition-all">
                  Accedi
                </router-link>
                <router-link to="/register" @click="isMobileMenuOpen = false" class="block w-full text-center py-4 rounded-2xl bg-blue-600 text-white text-lg font-black shadow-xl shadow-blue-500/30 transition-all">
                  Registrati Gratis
                </router-link>
              </div>
            </template>
          </div>
        </div>
      </transition>
    </nav>

    <!-- Telegram Promo Banner (Floating Tip) -->
    <transition
      enter-active-class="transition duration-500 ease-out"
      enter-from-class="transform translate-y-10 opacity-0 scale-95"
      enter-to-class="transform translate-y-0 opacity-100 scale-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="transform translate-y-0 opacity-100 scale-100"
      leave-to-class="transform translate-y-10 opacity-0 scale-95"
    >
      <div 
        v-if="isBannerVisible"
        class="fixed bottom-6 right-6 md:right-12 z-40 max-w-sm w-full"
      >
        <div class="bg-indigo-600 dark:bg-indigo-500 text-white rounded-2xl shadow-2xl p-4 flex items-center space-x-4 border border-indigo-400/30 backdrop-blur-md">
          <div class="flex-shrink-0 w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.12.02-1.96 1.25-5.54 3.69-.52.35-.99.53-1.39.52-.45-.01-1.31-.25-1.95-.45-.78-.25-1.4-.39-1.35-.82.02-.23.34-.46.95-.71 3.73-1.62 6.21-2.69 7.45-3.2 3.53-1.45 4.26-1.7 4.74-1.71.11 0 .34.03.5.15.13.11.17.26.19.38.01.07.02.21.01.28z"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold">Prezzi più bassi?</p>
            <p class="text-xs text-white/80">Unisciti al nostro canale Telegram!</p>
          </div>
          <a 
            href="https://t.me/amz_it_price_drop" 
            target="_blank"
            class="bg-white text-indigo-600 px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-indigo-50 transition-colors"
          >
            Apri
          </a>
          <button @click="isBannerVisible = false" class="text-white/60 hover:text-white transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </transition>
  </header>
</template>

<script>
import { jwtDecode } from 'jwt-decode'

export default {
    name: "HeaderTemplate",
    data() {
      return {
        isAuthenticated: false,
        isAdmin: false,
        isBannerVisible: true,
        isScrolled: false,
        isMobileMenuOpen: false,
        isAdminDropdownOpen: false,
        isAccountDropdownOpen: false,
        closeTimeouts: {
          admin: null,
          account: null
        }
      };
    },
    methods: {
      closeWithDelay(type) {
        this.closeTimeouts[type] = setTimeout(() => {
          if (type === 'admin') this.isAdminDropdownOpen = false;
          if (type === 'account') this.isAccountDropdownOpen = false;
        }, 150); // 150ms delay for better UX
      },
      clearCloseTimeout(type) {
        if (this.closeTimeouts[type]) {
          clearTimeout(this.closeTimeouts[type]);
          this.closeTimeouts[type] = null;
        }
      },
      getInitials() {
        const token = localStorage.getItem("token");
        if (!token) return 'U';
        try {
          const decoded = jwtDecode(token);
          return (decoded.sub || decoded.username || 'U').substring(0, 1).toUpperCase();
        } catch (e) {
          return 'U';
        }
      },
      handleScroll() {
        this.isScrolled = window.scrollY > 20;
      },
      checkAuth() {
        const token = localStorage.getItem("token");
        if (token) {
          try {
            const decoded = jwtDecode(token);
            const now = Math.floor(Date.now() / 1000);
            if (decoded.exp > now) {
              this.isAuthenticated = true;
              this.isAdmin = decoded.admin || false;
            } else {
              this.logout();
            }
          } catch (error) {
            console.error("Errore nella decodifica del token:", error);
            this.logout();
          }
        } else {
          this.isAuthenticated = false;
          this.isAdmin = false;
        }
      },
      logout() {
        localStorage.removeItem("token");
        this.isAuthenticated = false;
        this.isAdmin = false;
        this.$router.push("/login");
      },
      externalLink(to) {
        if (to === '/extension-download') {
          const apiBaseUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000';
          return `${apiBaseUrl}/api/extension/download`;
        }
        return to;
      }
    },
    mounted() {
      this.checkAuth();
      window.addEventListener('scroll', this.handleScroll);
    },
    beforeUnmount() {
      window.removeEventListener('scroll', this.handleScroll);
    },
    watch: {
      "$route"() {
        this.checkAuth();
        this.isMobileMenuOpen = false;
      },
    },
};
</script>

<style scoped>
.router-link-active {
  /* Using Tailwind for classes instead of scoped css when possible, but helper for clarity if needed */
}
</style>