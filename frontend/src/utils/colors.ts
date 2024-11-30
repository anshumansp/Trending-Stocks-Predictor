export const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'buy':
    case 'low':
    case 'success':
      return 'text-blue';
    case 'sell':
    case 'high':
    case 'error':
      return 'text-blue';
    case 'hold':
    case 'medium':
    case 'warning':
      return 'text-blue';
    default:
      return 'text-white';
  }
};
