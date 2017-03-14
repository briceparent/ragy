<!DOCTYPE html>
<html>
<head>
    <title>Ra.gy - Créateur de liens courts</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
</head>
<body>
<div class="container">
    <div class="row">
        <div class="col-sm-6 col-sm-offset-3">
            <header>
                <h1>
                    Ragy
                    <small>Créateur de liens courts</small>
                </h1>
            </header>
        </div>
    </div>
    % if message:
        <div class="row">
            <div class="col-sm-6 col-sm-offset-3">
                <div class="alert alert-{{ message.message_type }}">
                    % if message.icon:
                        <img src="{{ message.icon }}"/>
                    % end
                    {{ !message.message }}
                </div>
            </div>
        </div>
    % end
    <div class="row">
        <div class="col-sm-6 col-sm-offset-3">
            <form action="generate" method="POST">
                <div class="form-group">
                    <label>
                        Url à réduire :
                    </label>
                    <input class="form-control" type="url" required="required" name="link"
                           placeholder="http://votre-lien.com/page" value=""/>
                </div>

                <div class="form-group">
                    <label>
                        Choisir le lien court :
                    </label>
                    <div class="input-group">
                        <span class="input-group-addon" id="basic-addon1">http://ra.gy/</span>
                        <input class="form-control" name="id" pattern="^[a-zA-Z0-9_-]{5,10}"
                               placeholder="5 à 10 car." value="{{ next_id }}"/>
                        <span class="input-group-addon">(de 5 à 10 lettres et chiffres)</span>
                    </div>
                </div>

                <input type="submit" class="btn btn-primary btn-block" name="submit"
                       alt="Créer" value="Créer le lien"/>
            </form>
        </div>
    </div>
    <div class="row">
        <div class="col-sm-6 col-sm-offset-3">
            <br />
            <br />
            <br />
            <br />
            <footer style="color: #666;">
                Brought to you by
                <a href="https://www.linkedin.com/in/brice-parent/">Brice Parent</a>
            </footer>
        </div>
    </div>
</div>
</body>
</html>
