// var video = document.querySelector('video')
// let video = document.getElementById('video-watching')
addEventListener('seeking', (event) => {
  console.log(event)
})

addEventListener('offline', () => {
  alert('You are offline\nPlease get connected to continue watching')
})

addEventListener('online', () => {
  alert('You are now online!')
})