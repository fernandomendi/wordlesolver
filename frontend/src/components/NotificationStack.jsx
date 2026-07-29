// NotificationStack is a fixed top-right container for all overlay notifications.
// Children stack vertically; removing one causes the rest to shift up naturally
// via flexbox reflow.
export function NotificationStack({ children }) {
  return (
    <div className="fixed top-4 right-4 z-50 flex w-80 flex-col gap-2">
      {children}
    </div>
  )
}
