# frozen_string_literal: true

module WidgetHelper
  def find_role(role_id, linked_roles)
    linked_roles.find { |role| role["id"] == role_id }
  end

  def get_linked_role_for_person(person, linked_roles)
    role_id = person.dig("links", "roles", 0)
    find_role(role_id, linked_roles)
  end

  def should_render_initial_group?(group, initial_group_id, parent_group)
    group["id"] != initial_group_id && (!parent_group || parent_group["id"] != initial_group_id)
  end

  def should_render_parent_group?(parent_group)
    parent_group.present?
  end

  def should_render_children_groups?(children_groups)
    children_groups.any?
  end

  def sanitize_name(name)
    # Remove special characters and control characters, such as symbols, punctuation, and unassigned Unicode characters.
    name.encode("UTF-8", invalid: :replace, undef: :replace, replace: "").gsub(/[\p{So}\p{Cn}]/, "").strip
  end

  def extract_translation(multi_language_string, language)
    return nil unless multi_language_string

    translations = parse_translations(multi_language_string)
    get_translation(translations, language)
  end

  private

  def parse_translations(multi_language_string)
    translations = multi_language_string.split(" / ")
    {
      german: translations[0],
      french: translations[1],
      italian: translations[2],
      english: translations[3]
    }
  end

  def get_translation(translations, language)
    translations_mapping = {
      "fr" => :french,
      "it" => :italian,
      "en" => :english
    }

    translation_key = translations_mapping[language] || :german
    translations[translation_key] || translations[:german]
  end
end
