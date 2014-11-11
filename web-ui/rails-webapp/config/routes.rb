Rails.application.routes.draw do
  get 'dashboard/index'
  get 'dashboard/stats'
  get 'dashboard/settings'
  get 'dashboard/billing'
  get 'dashboard/support'
  get 'dashboard/insights'
  get 'dashboard/cloudconfig'  

get "static_controller/about"
authenticated do
  root :to => 'users#show', as: :authenticated, id: @resource
end
  root :to => 'visitors#index'
  devise_for :users
  resources :users
end
