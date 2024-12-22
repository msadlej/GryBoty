import * as React from "react"

const Alert = React.forwardRef(function Alert({ className, ...props }, ref) {
  return (
    <div
      ref={ref}
      role="alert"
      className={className}
      {...props}
    />
  )
})
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef(function AlertTitle({ className, ...props }, ref) {
  return (
    <h5
      ref={ref}
      className={className}
      {...props}
    />
  )
})
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef(function AlertDescription({ className, ...props }, ref) {
  return (
    <div
      ref={ref}
      className={className}
      {...props}
    />
  )
})
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }
