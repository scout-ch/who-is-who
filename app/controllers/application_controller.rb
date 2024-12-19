# frozen_string_literal: true

class ApplicationController < ActionController::Base
  # :nocov:
  unless Rails.env.test?
    ENV["BASIC_AUTH"].to_s.split(":").presence&.then do |username, password|
      http_basic_authenticate_with name: username, password: password
    end
  end
  # :nocov:
end
