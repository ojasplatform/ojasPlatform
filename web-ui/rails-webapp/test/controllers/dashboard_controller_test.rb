require 'test_helper'

class DashboardControllerTest < ActionController::TestCase
  test "should get index" do
    get :index
    assert_response :success
  end

  test "should get stats" do
    get :stats
    assert_response :success
  end

  test "should get settings" do
    get :settings
    assert_response :success
  end

  test "should get billing" do
    get :billing
    assert_response :success
  end

  test "should get support" do
    get :support
    assert_response :success
  end

end
