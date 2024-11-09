<template>
    <div>
      <h3>Storico dei Prezzi</h3>
      <ul>
        <li v-for="record in history" :key="record.date">
          {{ record.date }} - Prezzo: {{ record.price }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: ['history']
  }
  </script>
  