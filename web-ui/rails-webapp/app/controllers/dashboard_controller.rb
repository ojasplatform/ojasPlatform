class DashboardController < ApplicationController
  before_filter :authenticate_user!
  
  def index
    @user = User.find(params[:id])
  end

  def stats
    @user = User.find(params[:id])
  end
  
  def insights
    @user = User.find(params[:id])
  end

  def cloudconfig
    @user = User.find(params[:id])
  end
  
  def settings
    @user = User.find(params[:id])
  end

  def support
    @user = User.find(params[:id])
  end

  def billing
    @user = User.find(params[:id])
  end
  
end
