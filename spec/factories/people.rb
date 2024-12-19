# frozen_string_literal: true

Struct.new("PersonData", :id, :type, :href, :first_name, :last_name, :nickname, :email, :picture, :links)
Struct.new("LinkedRoles", :id, :role_type)
Struct.new("PeopleWithRoles", :people, :linked_roles)

FactoryBot.define do
  factory :person_data, class: "Struct::PersonData" do
    id { "17431" }
    type { "people" }
    href { "https://db.scout.ch/de/groups/9292/people/17431.json" }
    first_name { "John" }
    last_name { "Doe" }
    nickname { "Aragorn" }
    email { "aragorn@example.com" }
    picture { "https://image.com" }
    links do
      {
        "additional_emails" => ["111"],
        "phone_numbers" => ["1111111111"],
        "roles" => %w[1 2]
      }
    end

    initialize_with do
      new(id, type, href, first_name, last_name, nickname, email, picture, links)
    end
  end

  factory :linked_roles, class: "Struct::LinkedRoles" do
    id { "1" }
    role_type { "Leiter*in" }

    initialize_with { new(id, role_type) }
  end

  factory :other_linked_roles, class: "Struct::LinkedRoles" do
    id { "2" }
    role_type { "Mitglied" }

    initialize_with { new(id, role_type) }
  end

  factory :people_with_roles, class: "Struct::PeopleWithRoles" do
    people do
      [
        build(:person_data, id: "1", links: { "roles" => ["1"] }),
        build(:person_data, id: "2", links: { "roles" => ["2"] }),
        build(:person_data, id: "3", links: { "roles" => %w[1 2] })
      ]
    end
    linked_roles { [build(:linked_roles), build(:other_linked_roles)] }

    initialize_with { new(people, linked_roles) }
  end
end
