import blinpy as bp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
from pygam import LinearGAM, s
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import gammy
from gammy.arraymapper import x
from sklearn.model_selection import KFold

def fit_linear_regression(X, y, n_splits=5):

    # Set up K-Fold cross-validator
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Initialize lists to store performance metrics for each fold
    mse_list = []
    rmse_list = []
    mae_list = []
    r2_list = []

    # Create a figure to plot the results
    fig, axs = plt.subplots(n_splits, 1, figsize=(8, 4 * n_splits))

    # Iterate through each fold
    for idx, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, _ = X[train_index], X[test_index]
        y_train, _ = y.iloc[train_index], y.iloc[test_index]

        # Fit the linear regression model
        model = LinearRegression()
        model.fit(X_train.reshape(-1, 1), y_train)

        y_fit = model.predict(X_train.reshape(-1, 1))

        # Calculate performance metrics
        mse = mean_squared_error(y_train, y_fit)
        rmse = mean_squared_error(y_train, y_fit, squared=False)
        mae = mean_absolute_error(y_train, y_fit)
        r2 = r2_score(y_train, y_fit)

        # Store performance metrics
        mse_list.append(mse)
        rmse_list.append(rmse)
        mae_list.append(mae)
        r2_list.append(r2)

        # Plot the results for the current fold
        axs[idx].plot(X_train, y_train, 'b.', label='Data')
        axs[idx].plot(X_train, y_fit, 'r-', label='Fit')
        axs[idx].set_xlabel('x')
        axs[idx].set_title(f'Linear Regression (Fold {idx + 1})', fontsize=10)

    plt.tight_layout()

    # Calculate the average performance metrics across all folds
    performance = {
        'Model': ['Linear Regression'],
        'Mean Squared Error': [np.mean(mse_list)],
        'Root Mean Squared Error': [np.mean(rmse_list)],
        'Mean Absolute Error': [np.mean(mae_list)],
        'R2 Score': [np.mean(r2_list)]
    }

    return [pd.DataFrame(performance), fig]


## Random Forest Regressor
def fit_random_forest(X, y, n_splits=5):

    # Set up K-Fold cross-validator
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Initialize lists to store performance metrics for each fold
    mse_list = []
    rmse_list = []
    mae_list = []
    r2_list = []

    # Create a figure to plot the results
    fig, axs = plt.subplots(n_splits, 1, figsize=(8, 4 * n_splits))

    # Iterate through each fold
    for idx, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, _ = X[train_index], X[test_index]
        y_train, _ = y.iloc[train_index], y.iloc[test_index]

        # Fit the random forest model
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train.reshape(-1, 1), y_train)

        y_fit = model.predict(X_train.reshape(-1, 1))

        # Calculate performance metrics
        mse = mean_squared_error(y_train, y_fit)
        rmse = mean_squared_error(y_train, y_fit, squared=False)
        mae = mean_absolute_error(y_train, y_fit)
        r2 = r2_score(y_train, y_fit)

        # Store performance metrics
        mse_list.append(mse)
        rmse_list.append(rmse)
        mae_list.append(mae)
        r2_list.append(r2)

        # Plot the results for the current fold)
        axs[idx].plot(X_train, y_train, 'b.', label='Data')
        axs[idx].plot(X_train, y_fit, 'r-', label='Fit')
        axs[idx].set_xlabel('x')
        axs[idx].set_title(f'Random Forest (Fold {idx + 1})', fontsize=10)

    plt.tight_layout()

    # Calculate the average performance metrics across all folds
    performance = {
        'Model': ['Random Forest'],
        'Mean Squared Error': [np.mean(mse_list)],
        'Root Mean Squared Error': [np.mean(rmse_list)],
        'Mean Absolute Error': [np.mean(mae_list)],
        'R2 Score': [np.mean(r2_list)]
    }

    return [pd.DataFrame(performance), fig]

## Fit frequentist GAM
def fit_gam_regression(X, y, n_splits=5):

    # Set up K-Fold cross-validator
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Initialize lists to store performance metrics for each fold
    mse_list = []
    rmse_list = []
    mae_list = []
    r2_list = []

    # Create a figure to plot the results
    fig, axs = plt.subplots(n_splits, 1, figsize=(8, 4 * n_splits))

    # Iterate through each fold
    for idx, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, _ = X[train_index], X[test_index]
        y_train, _ = y.iloc[train_index], y.iloc[test_index]


        # Fit the Frequentist Penalized GAM
        gam_model = LinearGAM(s(0))
        gam_model.fit(X_train, y_train)
    
        yfit_gam = gam_model.predict(X_train)

        # Calculate performance metrics
        mse = mean_squared_error(y_train, yfit_gam)
        rmse = mean_squared_error(y_train, yfit_gam, squared=False)
        mae = mean_absolute_error(y_train, yfit_gam)
        r2 = r2_score(y_train, yfit_gam)

        # Store performance metrics
        mse_list.append(mse)
        rmse_list.append(rmse)
        mae_list.append(mae)
        r2_list.append(r2)

        # Plot the results for the current fold)
        axs[idx].plot(X_train, y_train, 'b.', label='Data')
        axs[idx].plot(X_train, yfit_gam, 'r-', label='Fit')
        axs[idx].set_xlabel('x')
        axs[idx].set_title(f'Frequentist Penalized Regression (Fold {idx + 1})', fontsize=10)
        
    plt.tight_layout()

    # Calculate the average performance metrics across all folds
    performance = {
        'Model': ['Frequentist Penalized Regression'],
        'Mean Squared Error': [np.mean(mse_list)],
        'Root Mean Squared Error': [np.mean(rmse_list)],
        'Mean Absolute Error': [np.mean(mae_list)],
        'R2 Score': [np.mean(r2_list)]
    }

    return [pd.DataFrame(performance), fig]


## Gaussian Process Priors 
def fit_gp_gammy_univariate(X, y, n_splits=5):

    # Set up K-Fold cross-validator
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Initialize lists to store performance metrics for each fold
    mse_list = {'exp square': [], 'rat quad': [], 'orn uhl': []}
    rmse_list = {'exp square': [], 'rat quad': [], 'orn uhl': []}
    mae_list = {'exp square': [], 'rat quad': [], 'orn uhl': []}
    r2_list = {'exp square': [], 'rat quad': [], 'orn uhl': []}

    fig, axs = plt.subplots(n_splits, 3, figsize=(12, 5 * n_splits))

    # Iterate through each fold
    for idx, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, _ = X[train_index], X[test_index]
        y_train, _ = y.iloc[train_index], y.iloc[test_index]

        grid = np.arange(0, 60, 0.1)
        corrlen = 10
        sigma = 700

        c = gammy.Scalar()

        # Define and fit models with different kernels 
        exp_squared_model = gammy.models.bayespy.GAM(
            gammy.ExpSquared1d(
                grid=grid,
                corrlen=corrlen,
                sigma=sigma,
                energy=0.9
            )(x) + c
        ).fit(X_train, y_train)
        rat_quad_model = gammy.models.bayespy.GAM(
            gammy.RationalQuadratic1d(
                grid=grid,
                corrlen=corrlen,
                alpha=1,
                sigma=sigma,
                energy=0.9
            )(x) + c
        ).fit(X_train, y_train)
        orn_uhl_model = gammy.models.bayespy.GAM(
            gammy.OrnsteinUhlenbeck1d(
                grid=grid,
                corrlen=corrlen,
                sigma=sigma,
                energy=0.9
            )(x) + c
        ).fit(X_train, y_train)

        exp_square_result = exp_squared_model.predict(X_train)
        rat_quad_result = rat_quad_model.predict(X_train)
        orn_uhl_result = orn_uhl_model.predict(X_train)

        # Calculate performance metrics
        mse_list['exp square'].append(mean_squared_error(y_train, exp_square_result))
        mse_list['rat quad'].append(mean_squared_error(y_train, rat_quad_result))
        mse_list['orn uhl'].append(mean_squared_error(y_train, orn_uhl_result))
        rmse_list['exp square'].append(mean_squared_error(y_train, exp_square_result, squared=False))
        rmse_list['rat quad'].append(mean_squared_error(y_train, rat_quad_result, squared=False))
        rmse_list['orn uhl'].append(mean_squared_error(y_train, orn_uhl_result, squared=False))
        mae_list['exp square'].append(mean_absolute_error(y_train, exp_square_result))
        mae_list['rat quad'].append(mean_absolute_error(y_train, rat_quad_result))
        mae_list['orn uhl'].append(mean_absolute_error(y_train, orn_uhl_result)) 
        r2_list['exp square'].append(r2_score(y_train, exp_square_result))
        r2_list['rat quad'].append(r2_score(y_train, rat_quad_result))
        r2_list['orn uhl'].append(r2_score(y_train, orn_uhl_result))

        axs[idx, 0].plot(X_train, y_train, 'b.', label='Data')
        axs[idx, 0].plot(X_train, exp_square_result, 'r-', label='Fit')
        axs[idx, 0].set_xlabel('x')
        axs[idx, 0].set_ylabel('y')
        axs[idx, 0].set_title(f'Exponential Squared (Fold {idx + 1})', fontsize=8)

        axs[idx, 1].plot(X_train, y_train, 'b.')
        axs[idx, 1].plot(X_train, rat_quad_result, 'r-')
        axs[idx, 1].set_xlabel('x')
        axs[idx, 1].set_title(f'Rational Quadratic (Fold {idx + 1})', fontsize=8)

        axs[idx, 2].plot(X_train, y_train, 'b.')
        axs[idx, 2].plot(X_train, orn_uhl_result, 'r-')
        axs[idx, 2].set_xlabel('x')
        axs[idx, 2].set_title(f'Ornstein-Uhlenbeck (Fold {idx + 1})', fontsize=8)

    # Calculate the average performance metrics across all folds
    performance = {
        'Model': ['exp square', 'rat quad', 'orn uhl'],
        'Mean Squared Error': [np.mean(mse_list['exp square']), np.mean(mse_list['rat quad']), np.mean(mse_list['orn uhl'])],
        'Root Mean Squared Error': [np.mean(rmse_list['exp square']), np.mean(rmse_list['rat quad']), np.mean(rmse_list['orn uhl'])],
        'Mean Absolute Error': [np.mean(mae_list['exp square']), np.mean(mae_list['rat quad']), np.mean(mae_list['orn uhl'])],
        'R2 Score': [np.mean(r2_list['exp square']), np.mean(r2_list['rat quad']), np.mean(r2_list['orn uhl'])]
    }

    performance_df = pd.DataFrame(performance)
    return [performance_df, fig]

def fit_difference_priors(X, y, n_splits=5):

    # Set up K-Fold cross-validator
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Initialize lists to store performance metrics for each fold
    mse_list = {'smooth': [], 'periodic': [], 'both': []}
    rmse_list = {'smooth': [], 'periodic': [], 'both': []}
    mae_list = {'smooth': [], 'periodic': [], 'both': []}
    r2_list = {'smooth': [], 'periodic': [], 'both': []}

    # Create a figure to plot the results
    fig, axs = plt.subplots(n_splits, 3, figsize=(9, 3 * n_splits))

    # Iterate through each fold
    for idx, (train_index, test_index) in enumerate(kf.split(X)):
        X_train, _ = X[train_index], X[test_index]
        y_train, _ = y.iloc[train_index], y.iloc[test_index]

        X_train = X_train.reshape(-1)
        y_train = np.array(y_train).reshape(-1)

        # Fit the GAM model with different priors
        generate_gam_spec = lambda B, pri_var: [
        {
            'fun': lambda df: bp.utils.interp_matrix(df['x'].values, X_train, sparse=False),
            'name': 'smoothfun',
            'prior': {
                'B': B,
                'mu': np.zeros(B.shape[0]),
                'cov': pri_var
            }
        }
        ]
        n = len(X_train)
        data = pd.DataFrame({'x': X_train, 'y': y_train})
        
        # case 1: just smoothness prior
        D_smooth = bp.utils.diffmat(n, order=2)
        var_smooth = 0.01*np.ones(D_smooth.shape[0])
        gam_spec_smooth = generate_gam_spec(D_smooth, var_smooth)

        # case 2: periodic smoothness prior
        D_periodic = bp.utils.diffmat(n, order=2, periodic=True)
        var_periodic = 0.01*np.ones(D_periodic.shape[0])
        gam_spec_periodic = generate_gam_spec(D_periodic, var_periodic)

        # symmetric prior
        D_symmetric = bp.utils.symmat(n, nsymm=np.where(X_train >= -np.pi/4)[0][0])
        var_symmetric = 0.01*np.ones(D_symmetric.shape[0])

        # case 3: periodic and symmetric priors combined
        D_per_symm = sparse.vstack((D_periodic, D_symmetric))
        var_per_symm = np.concatenate((var_periodic, var_symmetric))
        gam_spec_both = generate_gam_spec(D_per_symm, var_per_symm)

        smooth_result = bp.models.GamModel('y', gam_spec_smooth).fit(data, obs_cov=0.1).post_mu
        periodic_result = bp.models.GamModel('y', gam_spec_periodic).fit(data, obs_cov=0.1).post_mu
        both_result = bp.models.GamModel('y', gam_spec_both).fit(data, obs_cov=0.1).post_mu

        # Calculate the performance metrics
        mse_list['smooth'].append(mean_squared_error(y_train, smooth_result))
        mse_list['periodic'].append(mean_squared_error(y_train, periodic_result))
        mse_list['both'].append(mean_squared_error(y_train, both_result))
        mae_list['smooth'].append(mean_absolute_error(y_train, smooth_result))
        mae_list['periodic'].append(mean_absolute_error(y_train, periodic_result))
        mae_list['both'].append(mean_absolute_error(y_train, both_result))
        rmse_list['smooth'].append(mean_squared_error(y_train, smooth_result, squared=False))
        rmse_list['periodic'].append(mean_squared_error(y_train, periodic_result, squared=False))
        rmse_list['both'].append(mean_squared_error(y_train, both_result, squared=False))
        r2_list['smooth'].append(r2_score(y_train, smooth_result))
        r2_list['periodic'].append(r2_score(y_train, periodic_result))
        r2_list['both'].append(r2_score(y_train, both_result))

        # Plot the results
        axs[idx, 0].plot(X_train, y_train, 'b.', label='Data')
        axs[idx, 0].plot(X_train, smooth_result, 'r-', label='Fit')
        axs[idx, 0].set_title(f'Smooth (Fold {idx + 1})', fontsize=8)

        axs[idx, 1].plot(X_train, y_train, 'b.', label='Data')
        axs[idx, 1].plot(X_train, periodic_result, 'r-', label='Fit')
        axs[idx, 1].set_title(f'Smooth + Periodic (Fold {idx + 1})', fontsize=8)

        axs[idx, 2].plot(X_train, y_train, 'b.', label='Data')
        axs[idx, 2].plot(X_train, both_result, 'r-', label='Fit')
        axs[idx, 2].set_title(f'Smooth + Periodic + Symmetric (Fold {idx + 1})', fontsize=8)


    plt.tight_layout()

    # Performance
    performance = {
        'Model': ['smooth', 'periodic', 'both'],
        'Mean Squared Error': [np.mean(mse_list['smooth']), np.mean(mse_list['periodic']), np.mean(mse_list['both'])],
        'Root Mean Squared Error': [np.mean(rmse_list['smooth']), np.mean(rmse_list['periodic']), np.mean(rmse_list['both'])],
        'Mean Absolute Error': [np.mean(mae_list['smooth']), np.mean(mae_list['periodic']), np.mean(mae_list['both'])],
        'R2 Score': [np.mean(r2_list['smooth']), np.mean(r2_list['periodic']), np.mean(r2_list['both'])]
        }
    performance_df = pd.DataFrame(performance)
    return [performance_df, fig]