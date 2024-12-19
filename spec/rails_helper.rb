# frozen_string_literal: true

ENV["RAILS_ENV"] ||= "test"
require "spec_helper"
require_relative "../config/environment"
# Prevent database truncation if the environment is production
abort("The Rails environment is running in production mode!") if Rails.env.production?
require "rspec/rails"
require "capybara/rspec"
require "capybara/rails"
require "selenium/webdriver"
require "super_diff/rspec-rails"
require "webmock/rspec"

ActiveRecord::Migration.maintain_test_schema!

Rails.root.glob("spec/support/**/*.rb").each { |f| require f }

RSpec.configure do |config|
  config.include FactoryBot::Syntax::Methods
  config.include ActiveSupport::Testing::TimeHelpers

  config.use_transactional_fixtures = true
  config.infer_spec_type_from_file_location!

  config.before(:each, type: :system) do
    driven_by :rack_test
  end

  config.before(:all, type: :system) do
    Capybara.server = :puma, { Silent: true }
  end

  config.before(:each, :js, type: :system) do
    driven_by ENV["SELENIUM_DRIVER"]&.to_sym || :selenium_chrome_headless
  end

  config.before(:suite) do
    original_stderr = $stderr
    $stderr = StringIO.new

    at_exit do
      $stderr = original_stderr
    end
  end

  config.after do
    I18n.locale = I18n.default_locale
  end
end
