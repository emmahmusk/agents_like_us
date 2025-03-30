import 'package:collection/collection.dart';
Map<DateTime, num> calculateDailyContributionSums(List<Map<String, dynamic>> contributions) {
  if (contributions == null || contributions.isEmpty) {
    return {};
  }
  final isValid = contributions.every((contribution) =>
      contribution.containsKey('date') &&
      contribution.containsKey('amount') &&
      contribution['date'] is DateTime &&
      contribution['amount'] is num);
  if (!isValid) {
    return {}; 
  }
  return groupBy(contributions, (Map<String, dynamic> contribution) => contribution['date'] as DateTime)
      .map((date, contributionsForDate) => MapEntry(
          date,
          contributionsForDate.fold<num>(
              0, (sum, contribution) => sum + contribution['amount'] as num)));
}