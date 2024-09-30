package main

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Model holds the application's state.
type model struct {
	name    string
	entered bool
}

// Init is called when the program starts.
func (m model) Init() tea.Cmd {
	return nil
}

// Update is called when a key is pressed or other events occur.
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "enter":
			if !m.entered {
				m.entered = true
			} else {
				return m, tea.Quit
			}
		case "ctrl+c", "esc":
			return m, tea.Quit
		default:
			if !m.entered {
				m.name += msg.String()
			}
		}
	}

	return m, nil
}

// View is called to render the UI.
func (m model) View() string {
	if !m.entered {
		return inputStyle.Render("Enter your name: ") + m.name
	}

	greeting := fmt.Sprintf("Hello, %s!", m.name)
	return greetingStyle.Render(greeting)
}

var (
	inputStyle    = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
	greetingStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("212"))
)

func main() {
	// Initialize the model
	m := model{}

	// Start the Bubble Tea program
	p := tea.NewProgram(m)

	// Run the program
	if err := p.Start(); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
}
