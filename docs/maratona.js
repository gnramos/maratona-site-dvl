const CONFIG = {current: {year: '2023', phaseDir: ''},
                rules: [{class: 'text-warning'},
                        {class: 'text-danger', tooltip: 'Top 15!'},
                        {class: 'text-primary', tooltip: 'Distribuição por sedes.'},
                        {class: 'text-success', tooltip: 'Vagas discricionárias.'},
                        {class: 'regra4', tooltip: 'Vagas femininas.'}],
                phases: [{name: 'Fase Zero', dir: 'Zero', start: 2022},
                         {name: '1ª Fase', dir: 'Primeira', start: 2004},
                         {name: 'Final Nacional', dir: 'Nacional', start: 1996},
                         {name: 'Campeonato Latino-Americano', dir: 'LatAm', start: 2023},
                         {name: 'Final Mundial', dir: 'Mundial', start: 1989}],
                schools: {chart: {show_last_years: 5}}};
/******************************************************************************/

/**
 * Create a contact link.
 *
 * @param  {String} text the text to show as link
 * @param  {String} args parts of the string that compose de e-mail address
 * @return {String}      the HTML with the formatted information
 */
function contact(text, ...args) {
    let address = args.reduce((acc, cur) => acc + cur);
    // html HEX character encoding
    return `<a href="&#x6d;&#x61;&#x69;&#x6c;&#x74;&#x6f;&#58;${address}">${text}</a>`;
}

/**
 * Returns the relative path to the root of the files.
 */
function root() {
  let url = window.location.pathname.split('/');
  // return '../'.repeat(url.length - 9);
  return '/maratona-site-dvl/';
}

/**
 * Create page header.
 *
 * @param  {String} pageTitle   page title
 * @param  {String} breadcrumbs breadcrumbs to page
 * @return {String}             the HTML with the formatted information
 */
function bodyHeader(pageTitle='', breadcrumbs='') {
  let url = window.location.pathname.split('/');

  function aboutItem(isActive) {
    return `
<li class="nav-item dropdown">
  <a class="nav-link dropdown-toggle ${isActive ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
    Sobre
  </a>
  <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
    <li><a class="dropdown-item" href="${root()}sobre/index.html">O que é?</a></li>
    <li><a class="dropdown-item" href="${root()}sobre/regras.html">Regras</a></li>
    <li><a class="dropdown-item" href="${root()}sobre/ambiente_computacional.html">Ambiente Computacional</a></li>
    <li><a class="dropdown-item" href="${root()}sobre/organizacao.html">Organização</a></li>
    <li><a class="dropdown-item" href="${root()}sobre/divulgacao.html">Divulgação</a></li>
  </ul>
</li>`;
  }
  function participateItem(isActive) {
    let phaseLinks = '';
    if (CONFIG.current.phaseDir != '') {
      for (i in CONFIG.phases) {
        phaseLinks += `
    <li><a class="dropdown-item" href="${root()}eventos/${CONFIG.current.year}/${CONFIG.phases[i].dir}/index.html">${CONFIG.phases[i].name}</a></li>`;
        if (CONFIG.phases[i].dir == CONFIG.current.phaseDir)
          break;
      }
    }

    return `
<li class="nav-item dropdown">
  <a class="nav-link dropdown-toggle ${isActive ? 'active' : ''}" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
    Participe!
  </a>
  <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
    <li><a class="dropdown-item" href="${root()}inscricoes.html"><strong>Inscrições</strong></a></li>
    <li><hr class="dropdown-divider"></li>
${phaseLinks}
  </ul>
</li>`;
}
  function historyItem(isActive) {
    return `<li class="nav-item">
  <a href="${root()}hist/index.html" class="nav-link${isActive ? ' active" aria-current="page"' : ''}">Histórico</a>
</li>`;
}
  function contactItem(isActive) {
    return `<li class="nav-item">
  <a href="${root()}contato.html" class="nav-link${isActive ? ' active" aria-current="page"' : ''}">Contato</a>
</li>`
}
  let socialMediaItems = `
<li class="nav-item">
  <a href="https://www.facebook.com/maratona/" class="nav-link">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
      <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
    </svg>
  </a>
</li>
<li class="nav-item">
  <a href="https://www.youtube.com/channel/UCuLfhw7dJoKYbzBktNRgAkA" class="nav-link">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
      <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
    </svg>
  </a>
</li>`;

  return`
    <div class="container">
      <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
        <a href="${root()}index.html" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
          <img src="${root()}img/maratona-logo.jpg" class="bi me-2" height="32">
          <span class="fs-4">Maratona de Programação</span>
        </a>
        <ul class="nav nav-pills">
          ${aboutItem(url.includes('sobre'))}
          ${participateItem(url.includes('inscricoes.html') || url.includes(CONFIG.current.year))}
          ${historyItem(!url.includes(CONFIG.current.year) && (url.includes('eventos') || url.includes('escolas') || url.includes('hist')))}
          ${contactItem(url.includes('contato.html'))}
          ${socialMediaItems}
        </ul>
      </header>
    </div>
    <div class="container text-left">
      ${breadcrumbs}
      <h1>${pageTitle}</h1>`;
}

/**
 * Create page footer.
 *
 * @return {String} the HTML with the formatted information
 */
function bodyFooter() {
  return `
    </div>
    <div class="container">
      <footer class="footer mt-auto py-3 justify-content-center border-top">
        <div class="container">
          <div class="row">
            <div class="col-sm-2">
              Realização:
            </div>
            <div class="col-sm-3">
              <a href="${root()}sobre/sbc.html"><img src="${root()}img/footer_SBC.png" class="img-fluid"></a>
            </div>
            <div class="col-sm-7">
              <a href="https://icpc.global/"><img src="${root()}img/footer_ICPC.jpg" class="img-fluid"></a>
            </div>
          </div>
        </div>
      </footer>
    </div`;
}

/**
 * Create an accordion with the given items.
 *
 * Creates a Bootstrap Accordion (https://getbootstrap.com/docs/5.0/components/accordion/).
 *
 * @param  {String}  name          the ID for the accordion
 * @param  {Array}   items         an array with the content for each accordion item, which should be formatted as an Array [headerText, bodyText]
 * @param  {Array}   headerClasses an array with additional class information for each item header
 * @param  {boolean} collapseFirst a boolean indicating whether to collapse the first item
 * @return {String}                the HTML with the formatted information
 */
function accordion(name, items, headerClasses=[], collapseFirst=true) {
  let accItems = '';
  for (i in items) {
    accItems += `
  <div class="accordion-item">
    <h2 class="accordion-header" id="heading${name + i}">
      <button class="accordion-button ${collapseFirst ? 'collapsed' : ''} ${headerClasses[i] != undefined ? headerClasses[i] : ''}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${name + i}" aria-expanded="false" aria-controls="collapse${name + i}">
        ${items[i][0]}
      </button>
    </h2>
    <div id="collapse${name + i}" class="accordion-collapse collapse ${collapseFirst ? '' : 'show'}" aria-labelledby="heading${name + i}" data-bs-parent="#accordion${name}">
      <div class="accordion-body">
        ${items[i][1]}
      </div>
    </div>
  </div>`;
    if (!collapseFirst) collapseFirst = true;
  }

  return `
<div class="accordion" id="accordion${name}">
  ${accItems}
</div>`;
}

/**
 * Create a carousel with the given images.
 *
 * Creates a Bootstrap Carousel (https://getbootstrap.com/docs/5.0/components/carousel/).
 *
 * @param  {Array}  images an array with the paths for each image
 * @return {String}        the HTML with the formatted information
 */
function carousel(images) {
  let items = '';
  for (i in images)
    items += `
  <div class="carousel-item ${i == 0 ? 'active' : ''}">
    <img src="${images[i]}" class="d-block w-100" style="object-fit: scale-down;">
  </div>`;

  return `
<div id="carouselCaptions" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-inner">
    ${items}
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselCaptions" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselCaptions" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>`;
}

/**
 * Return a list with the given items.
 *
 * @param  {String} type        type of list (ul, ol)
 * @param  {Array}  items       array with items to be listed
 * @param  {String} listOptions list options
 * @param  {String} itemOptions item options
 * @return {String}             the HTML with the formatted information
 */
function makeList(type, items, listOptions='', itemOptions=[]) {
  let listItems = '';
  for (i in items)
    listItems += `\n<li ${itemOptions[i]}>${items[i]}</li>`;
  return `\n<${type} ${listOptions}>${listItems}\n</${type}>`;
}

/**
 * Return a list  of links.
 *
 * Assumes the links are formatted as a list of [url, text] items.
 *
 * @param  {Array}  links       array with links to be listed, each in the [link, text] format
 * @param  {String} type        type of list (ul, ol)
 * @param  {String} listOptions list options
 * @param  {String} itemOptions item options
 * @return {String}             the HTML with the formatted information
 */
function listLinks(links, type='ul', listOptions='', itemOptions=[]) {
  let items = [];
  for (link of links)
    items.push(`<a href="${link[0]}">${link[1]}</a>`);
  return makeList(type, items, listOptions, itemOptions);
}

/**
 * Return the full name of the event (with roman numerals).
 */
function fullName(year, suffix='') {
  // https://stackoverflow.com/questions/9083037/convert-a-number-into-a-roman-numeral-in-javascript
  const NUMERAL_CODES = [["","I","II","III","IV","V","VI","VII","VIII","IX"],  // Ones
                         ["","X","XX","XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]];  // Tens
  let numeral = '', digits = (year - 1995).toString().split('').reverse();
  for (let i = 0; i < digits.length; i++)
    numeral = NUMERAL_CODES[i][parseInt(digits[i])] + numeral;

  return `${numeral} Maratona SBC de Programação${suffix}`
}
