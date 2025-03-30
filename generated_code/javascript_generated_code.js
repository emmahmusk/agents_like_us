const calculateDailyContributionSums = (contributions) => {
  if (!Array.isArray(contributions) || contributions.length === 0) {
    return new Map();
  }
  const isValidContribution = (contrib) => contrib.hasOwnProperty('date') && contrib.hasOwnProperty('amount') && contrib.date instanceof Date && typeof contrib.amount === 'number';
  if (!contributions.every(isValidContribution)) {
    return new Map();
  }
  const dailySums = new Map();
  contributions.forEach(contribution => {
    const dateString = contribution.date.toISOString().slice(0, 10); 
    const currentSum = dailySums.get(dateString) || 0;
    dailySums.set(dateString, currentSum + contribution.amount);
  });
  return dailySums;
};