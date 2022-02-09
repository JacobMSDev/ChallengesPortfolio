#include "Shader.h"

Shader::Shader()
	: m_shaderID{ glCreateProgram() }
{

}

/*\
 * Takes in the name of a vertex and fragment shader file
 * and generates and binds a shader program.
\*/
void Shader::newVFShader(const std::string& vertexName, const std::string& fragmentName)
{
	std::string shaderName{ "" };
	compileShader(GL_VERTEX_SHADER, getSourceFromFile(vertexName, shaderName).c_str(), shaderName);
	compileShader(GL_FRAGMENT_SHADER, getSourceFromFile(fragmentName, shaderName).c_str(), shaderName);
	glLinkProgram(m_shaderID);
	bind();
}

/*\
 * Takes a shader type (E.g. GL_VERTEX_SHADER), a c-style string
 * for the source code and the name of the shader and compiles it
 * ready to be bound into a full program.
\*/
void Shader::compileShader(const GLuint type, const char* source, const std::string& shaderName)
{
	unsigned int shader;
	shader = glCreateShader(type);
	glShaderSource(shader, 1, &source, NULL);
	glCompileShader(shader);

	int success;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		std::cout << "ERROR IN SHADER " << shaderName << " COMPILATION_FAILED\n" << std::endl;
		char infoLog[512];
		glGetShaderInfoLog(shader, 512, NULL, infoLog);
		std::cout << infoLog << std::endl;
	};

	glAttachShader(m_shaderID, shader);
	glDeleteShader(shader);
}

/*\
 * Takes in a file path and retrieves and then returns a
 * shader source code from the file.
 * Additionally, stores the shaders name (defined in the
 * shader source like <NAME HERE>) in the variable
 * shaderRef to be used elsewhere.
\*/
std::string Shader::getSourceFromFile(const std::string& shaderName, std::string& shaderRef)
{
	std::string source{ "" };
	std::string line{ "" };
	// Open shader source file
	std::ifstream sourceText( findShaderSourcePath() + shaderName + ".shader", std::ios::ate );

	if (sourceText)
	{
		// Determine the size of the file to reserve space
		// in 'source' to stop memory reallocations
		std::ifstream::streampos fileSize = sourceText.tellg();
		source.reserve(fileSize);
		sourceText.seekg(0);
		
		// Clear first line of file and store value in shaderRef
		getline(sourceText, line);
		shaderRef = line;

		// Extract each line from the input file and place in 'source'
		while (getline(sourceText, line)) {
			if (line != "") {
				source += line + "\n";
			}
		}
	}
	else
	{
		std::cout << "FILE NOT FOUND!\n";
	}

	return source;
}

/*\
 * Bind this as the active shader
\*/
void Shader::bind()
{
	glUseProgram(m_shaderID);
}

/*\
 * Return the ID of the shader program
\*/
unsigned int Shader::getID()
{
	return m_shaderID;
}

/*\
 * Determine the location of the .shader files.
 * 
 * Only to be used in debug builds and not
 * for production builds.
\*/
std::string findShaderSourcePath()
{
	// Static to avoid caluclating multiple times
	static std::string sourcePath{ "" };

	// Test if the source path has
	// already been found once
	if (sourcePath == "") {
		sourcePath = __FILE__;
		int ind = sourcePath.size();
		int foundSlashes = 0;
		
		// Search for first two / character 
		// in order to remove filename and first folder
		while (--ind > 0)
		{
			if (sourcePath[ind] == '\\')
			{
				++foundSlashes;
				if (foundSlashes > 1)
				{
					break;
				}
			}
		}
		// Append the shader folder to the path
		sourcePath.erase(++ind);
		sourcePath += "Shaders\\";
	}

	return sourcePath;
}
