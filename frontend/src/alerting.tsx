export const alert_options = {
  insert: "top" as const,
  container: "top-right" as const,
  animationIn: ["animate__animated", "animate__fadeIn"],
  animationOut: ["animate__animated", "animate__fadeOut"],
  dismiss: {
    duration: 4000,
    onScreen: false,
    pauseOnHover: true
  }
}