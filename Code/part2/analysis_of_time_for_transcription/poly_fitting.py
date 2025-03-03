

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error

# # Train dataset
# train_durations = np.array([1.02, 3.03, 5.01, 10.02, 20.01, 30.0, 40.02, 50.01, 60.0, 125.01, 280.02, 650.01, 1801.14])
# train_time_taken = np.array([1.8068888187408447, 2.0778377056121826, 2.72623610496521, 2.912597179412842, 4.800200700759888, 
#                              7.316509962081909, 8.122992753982544, 9.500887870788574, 13.072041273117065, 27.45095133781433, 
#                              57.35416603088379, 135.15591168403625, 366.500568151474])

# # Test dataset
# test_durations = np.array([350.55, 15.03, 900.03, 1250.58, 1200.06, 90.0, 200.01, 35.01, 8.01, 400.02])
# test_time_taken = np.array([70.62015891075134, 3.5125882625579834, 182.81184077262878, 255.48256468772888, 
#                             253.59933614730835, 18.18311643600464, 41.350902795791626, 8.046822309494019, 
#                             2.5601205825805664, 82.40970182418823])

# # Fit polynomials of degree 1, 2, and 3
# p1 = np.polyfit(train_durations, train_time_taken, 1)  # Linear
# p2 = np.polyfit(train_durations, train_time_taken, 2)  # Quadratic
# p3 = np.polyfit(train_durations, train_time_taken, 3)  # Cubic

# # Predictions on train data
# y_train_pred1 = np.polyval(p1, train_durations)
# y_train_pred2 = np.polyval(p2, train_durations)
# y_train_pred3 = np.polyval(p3, train_durations)

# # Predictions on test data
# y_test_pred1 = np.polyval(p1, test_durations)
# y_test_pred2 = np.polyval(p2, test_durations)
# y_test_pred3 = np.polyval(p3, test_durations)

# # Compute Mean Squared Error (MSE)
# mse_train1 = mean_squared_error(train_time_taken, y_train_pred1)
# mse_train2 = mean_squared_error(train_time_taken, y_train_pred2)
# mse_train3 = mean_squared_error(train_time_taken, y_train_pred3)

# mse_test1 = mean_squared_error(test_time_taken, y_test_pred1)
# mse_test2 = mean_squared_error(test_time_taken, y_test_pred2)
# mse_test3 = mean_squared_error(test_time_taken, y_test_pred3)

# # Print MSE values
# print(f"Train MSE for 1st Degree Polynomial: {mse_train1:.5f}")
# print(f"Test  MSE for 1st Degree Polynomial: {mse_test1:.5f}\n")

# print(f"Train MSE for 2nd Degree Polynomial: {mse_train2:.5f}")
# print(f"Test  MSE for 2nd Degree Polynomial: {mse_test2:.5f}\n")

# print(f"Train MSE for 3rd Degree Polynomial: {mse_train3:.5f}")
# print(f"Test  MSE for 3rd Degree Polynomial: {mse_test3:.5f}\n")

# # Generate x values for smooth curve plotting
# x_vals = np.linspace(min(train_durations), max(train_durations), 500)
# y1 = np.polyval(p1, x_vals)
# y2 = np.polyval(p2, x_vals)
# y3 = np.polyval(p3, x_vals)

# # Plot the data and the fitted curves
# plt.scatter(train_durations, train_time_taken, color='black', label="Train Data", zorder=3)
# plt.scatter(test_durations, test_time_taken, color='purple', label="Test Data", marker="x", zorder=3)
# plt.plot(x_vals, y1, label="1st Degree (Linear)", linestyle="dashed", color='red')
# plt.plot(x_vals, y2, label="2nd Degree (Quadratic)", linestyle="dashed", color='blue')
# plt.plot(x_vals, y3, label="3rd Degree (Cubic)", linestyle="dashed", color='green')

# # Labels and title
# plt.xlabel("Durations")
# plt.ylabel("Time Taken")
# plt.title("Polynomial Regression: Time Taken vs Durations")
# plt.legend()
# plt.grid(True, linestyle="--", alpha=0.6)
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Train dataset
train_durations = np.array([1.02, 3.03, 5.01, 10.02, 20.01, 30.0, 40.02, 50.01, 60.0, 125.01, 280.02, 650.01, 1801.14])
train_time_taken = np.array([1.8068888187408447, 2.0778377056121826, 2.72623610496521, 2.912597179412842, 4.800200700759888, 
                             7.316509962081909, 8.122992753982544, 9.500887870788574, 13.072041273117065, 27.45095133781433, 
                             57.35416603088379, 135.15591168403625, 366.500568151474])

# Test dataset
test_durations = np.array([350.55, 15.03, 900.03, 1250.58, 1200.06, 90.0, 200.01, 35.01, 8.01, 400.02])
test_time_taken = np.array([70.62015891075134, 3.5125882625579834, 182.81184077262878, 255.48256468772888, 
                            253.59933614730835, 18.18311643600464, 41.350902795791626, 8.046822309494019, 
                            2.5601205825805664, 82.40970182418823])

# Fit polynomials of degree 1, 2, and 3
p1 = np.polyfit(train_durations, train_time_taken, 1)  # Linear
p2 = np.polyfit(train_durations, train_time_taken, 2)  # Quadratic
p3 = np.polyfit(train_durations, train_time_taken, 3)  # Cubic

# Generate x values for smooth curve plotting (random sample points)
x_vals = np.linspace(min(train_durations), max(train_durations), 500)

# Polynomial functions
def poly1(x): return np.polyval(p1, x)
def poly2(x): return np.polyval(p2, x)
def poly3(x): return np.polyval(p3, x)

# Compute Train & Test MSE
mse_train1 = mean_squared_error(train_time_taken, poly1(train_durations))
mse_train2 = mean_squared_error(train_time_taken, poly2(train_durations))
mse_train3 = mean_squared_error(train_time_taken, poly3(train_durations))

mse_test1 = mean_squared_error(test_time_taken, poly1(test_durations))
mse_test2 = mean_squared_error(test_time_taken, poly2(test_durations))
mse_test3 = mean_squared_error(test_time_taken, poly3(test_durations))

# Print MSE values
print(f"Train MSE for 1st Degree Polynomial: {mse_train1:.5f}")
print(f"Test  MSE for 1st Degree Polynomial: {mse_test1:.5f}\n")

print(f"Train MSE for 2nd Degree Polynomial: {mse_train2:.5f}")
print(f"Test  MSE for 2nd Degree Polynomial: {mse_test2:.5f}\n")

print(f"Train MSE for 3rd Degree Polynomial: {mse_train3:.5f}")
print(f"Test  MSE for 3rd Degree Polynomial: {mse_test3:.5f}\n")

# 📌 Main Plot: Train & Test Data with All Curves
plt.figure(figsize=(8, 5))
plt.scatter(train_durations, train_time_taken, color='black', label="Train Data", zorder=3)
plt.scatter(test_durations, test_time_taken, color='purple', label="Test Data", marker="x", zorder=3)
plt.plot(x_vals, poly1(x_vals), label="1st Degree (Linear)", linestyle="dashed", color='red')
plt.plot(x_vals, poly2(x_vals), label="2nd Degree (Quadratic)", linestyle="dashed", color='blue')
plt.plot(x_vals, poly3(x_vals), label="3rd Degree (Cubic)", linestyle="dashed", color='green')
plt.xlabel("Durations")
plt.ylabel("Time Taken")
plt.title("Polynomial Regression: Time Taken vs Durations")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# 📌 Separate plots for each polynomial equation
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 1st Degree Polynomial
axes[0].plot(x_vals, poly1(x_vals), color='red', label="1st Degree Fit")
axes[0].scatter(train_durations, train_time_taken, color='black', label="Train Data")
axes[0].scatter(test_durations, test_time_taken, color='purple', marker="x", label="Test Data")
axes[0].set_title("1st Degree Polynomial")
axes[0].set_xlabel("Durations")
axes[0].set_ylabel("Time Taken")
axes[0].legend()
axes[0].grid(True, linestyle="--", alpha=0.6)

# 2nd Degree Polynomial
axes[1].plot(x_vals, poly2(x_vals), color='blue', label="2nd Degree Fit")
axes[1].scatter(train_durations, train_time_taken, color='black', label="Train Data")
axes[1].scatter(test_durations, test_time_taken, color='purple', marker="x", label="Test Data")
axes[1].set_title("2nd Degree Polynomial")
axes[1].set_xlabel("Durations")
axes[1].legend()
axes[1].grid(True, linestyle="--", alpha=0.6)

# 3rd Degree Polynomial
axes[2].plot(x_vals, poly3(x_vals), color='green', label="3rd Degree Fit")
axes[2].scatter(train_durations, train_time_taken, color='black', label="Train Data")
axes[2].scatter(test_durations, test_time_taken, color='purple', marker="x", label="Test Data")
axes[2].set_title("3rd Degree Polynomial")
axes[2].set_xlabel("Durations")
axes[2].legend()
axes[2].grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()
