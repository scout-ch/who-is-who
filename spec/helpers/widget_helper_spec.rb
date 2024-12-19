# frozen_string_literal: true

require "rails_helper"

RSpec.describe WidgetHelper, type: :helper do
  describe "#sanitize_name" do
    it "removes emojis from the name" do
      name_with_emoji = "John Doe 😀"
      expect(helper.sanitize_name(name_with_emoji)).to eq("John Doe")
    end

    it "retains special characters like ö" do
      name_with_special_char = "Jörg"
      expect(helper.sanitize_name(name_with_special_char)).to eq("Jörg")
    end
  end

  describe "#extract_translation" do
    let(:multi_language_string) { "Hallo / Bonjour / Ciao / Hello" }

    it "returns the German translation when language is de" do
      expect(helper.extract_translation(multi_language_string, "de")).to eq("Hallo")
    end

    it "returns the French translation when language is fr" do
      expect(helper.extract_translation(multi_language_string, "fr")).to eq("Bonjour")
    end

    it "returns the Italian translation when language is it" do
      expect(helper.extract_translation(multi_language_string, "it")).to eq("Ciao")
    end

    it "returns the English translation when language is en" do
      expect(helper.extract_translation(multi_language_string, "en")).to eq("Hello")
    end

    it "returns the German translation when language is unknown" do
      expect(helper.extract_translation(multi_language_string, "es")).to eq("Hallo")
    end

    it "returns nil when multi_language_string is nil" do
      expect(helper.extract_translation(nil, nil)).to be_nil
    end
  end

  describe "#get_linked_role_for_person" do
    let(:linked_roles) { [{ "id" => 1, "name" => "Leader" }, { "id" => 2, "name" => "Member" }] }

    it "returns the correct role for the person" do
      person = { "links" => { "roles" => [1] } }
      expect(helper.get_linked_role_for_person(person, linked_roles)).to eq({ "id" => 1, "name" => "Leader" })
    end

    it "returns nil if the role is not found" do
      person = { "links" => { "roles" => [3] } }
      expect(helper.get_linked_role_for_person(person, linked_roles)).to be_nil
    end

    it "returns nil if the person has no roles" do
      person = { "links" => { "roles" => [] } }
      expect(helper.get_linked_role_for_person(person, linked_roles)).to be_nil
    end

    it "returns nil if the person has no links" do
      person = {}
      expect(helper.get_linked_role_for_person(person, linked_roles)).to be_nil
    end
  end
end
